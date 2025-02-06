import time
import board
import pwmio
import digitalio
from ov7670 import OV7670_30x40_RGB565 as Camara

servo_hombro = pwmio.PWMOut(board.GP10, duty_cycle=0, frequency=50)
servo_codo = pwmio.PWMOut(board.GP11, duty_cycle=0, frequency=50)

electroiman = digitalio.DigitalInOut(board.GP16)
electroiman.direction = digitalio.Direction.OUTPUT
ciclo_min = 1638  
ciclo_max = 8192 
camara = Camara(
    d0_d7pinslist=[board.GP0, board.GP1, board.GP2, board.GP3,
                   board.GP4, board.GP5, board.GP6, board.GP7],
    plk=board.GP8,
    xlk=board.GP9,
    sda=board.GP20,
    scl=board.GP21,
    hs=board.GP12,
    vs=board.GP13,
    ret=board.GP14,
    pwdn=board.GP15
)


def bezier(t, P0, P1, P2, P3):
    return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3


def mover_servo_suave(pwm, angulo_inicio, angulo_fin, pasos=150, duracion=1.5):
    P0, P1, P2, P3 = angulo_inicio, angulo_inicio + (angulo_fin - angulo_inicio) / 3, angulo_fin - (angulo_fin - angulo_inicio) / 3, angulo_fin
    for i in range(pasos + 1):
        t = i / pasos
        angulo_actual = bezier(t, P0, P1, P2, P3)
        duty_cycle = max(min(int(ciclo_min + (angulo_actual / 180) * (ciclo_max - ciclo_min)), ciclo_max), ciclo_min)
        pwm.duty_cycle = duty_cycle
        time.sleep(duracion / pasos)


def bajar_al_piso():
    print("Bajando electroimán al suelo...")
    mover_servo_suave(servo_hombro, 90, 180)  
    mover_servo_suave(servo_codo, 90, 180)  
    time.sleep(1)


def activar_electroiman():
    print("Electroimán activado")
    electroiman.value = True
    time.sleep(2)

def desactivar_electroiman():
    print("Electroimán desactivado")
    electroiman.value = False
    time.sleep(1)

def detectar_color():
    try:
       
        buffer = camara()
        azul_count = 0
        rojo_count = 0
        verde_count = 0

        
        for i in range(0, len(buffer), 2):
            
            rgb565 = (buffer[i] << 8) | buffer[i + 1]
            r = ((rgb565 >> 11) & 0x1F) * 8   
            g = ((rgb565 >> 5) & 0x3F) * 4    
            b = (rgb565 & 0x1F) * 8           

            
            if b > 50 and b > (r + 3) and b > (g + 3):  
                azul_count += 1
            elif r > 140 and r > (g + 60) and r > (b + 60):  
                rojo_count += 1
            elif g > 120 and g > (r + 50) and g > (b + 50):  
                verde_count += 1

       
        if azul_count > rojo_count and azul_count > verde_count:
            return "azul"
        elif rojo_count > azul_count and rojo_count > verde_count:
            return "rojo"
        elif verde_count > azul_count and verde_count > rojo_count:
            return "verde"
        else:
            return None
    except Exception as e:
        print("Error al capturar la imagen o procesar los datos:", e)
        return None


def movimiento_azul():
    print("Ejecutando movimiento azul")
    bajar_al_piso()
    activar_electroiman()
    mover_servo_suave(servo_hombro, 180, 90)
    mover_servo_suave(servo_codo, 180, 90)
    desactivar_electroiman()
    mover_servo_suave(servo_hombro, 90, 90)
    mover_servo_suave(servo_codo, 90, 90)

def movimiento_rojo():
    print("Ejecutando movimiento rojo")
    bajar_al_piso()
    activar_electroiman()
    mover_servo_suave(servo_hombro, 180, 90)
    mover_servo_suave(servo_codo, 180, 90)
    desactivar_electroiman()
    mover_servo_suave(servo_hombro, 120, 120)  
    mover_servo_suave(servo_codo, 120, 120)  #

def movimiento_verde():
    print("Ejecutando movimiento verde")
    bajar_al_piso()
    activar_electroiman()
    mover_servo_suave(servo_hombro, 180, 90)
    mover_servo_suave(servo_codo, 180, 90)
    desactivar_electroiman()
    mover_servo_suave(servo_hombro, 150, 150)
    mover_servo_suave(servo_codo, 150, 150)


while True:
    color_detectado = detectar_color()
    print(f"Color detectado: {color_detectado}")
    if color_detectado == "azul":
        print("Esperando 1 segundos para confirmar color azul...")
        time.sleep(1)
        movimiento_azul()
    elif color_detectado == "rojo":
        print("Esperando 1 segundos para confirmar color rojo...")
        time.sleep(1)
        movimiento_rojo()
    elif color_detectado == "verde":
        print("Esperando 1 segundos para confirmar color verde...")
        time.sleep(1)
        movimiento_verde()

    time.sleep(5)