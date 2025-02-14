import time
import board
import pwmio
import digitalio
from ov7670 import OV7670_30x40_RGB565 as Camara

# Definición de servos
servo_base = pwmio.PWMOut(board.GP17, duty_cycle=0, frequency=50)
servo_hombro = pwmio.PWMOut(board.GP10, duty_cycle=0, frequency=50)
servo_codo = pwmio.PWMOut(board.GP11, duty_cycle=0, frequency=50)

# Electroimán
electroiman = digitalio.DigitalInOut(board.GP16)
electroiman.direction = digitalio.Direction.OUTPUT

# Valores de ciclo de trabajo para PWM
ciclo_min = 1638  
ciclo_max = 8192 

# Configuración de la cámara
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

# Diccionario para almacenar las posiciones detectadas y sus tiempos
posiciones_detectadas = {}
tiempo_ultima_deteccion = {}  # Almacena el último tiempo de detección por ángulo

def bezier(t, P0, P1, P2, P3):
    return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3

def mover_servo_suave(pwm, angulo_inicio, angulo_fin, pasos=100, duracion=1.0):
    for i in range(pasos + 1):
        t = i / pasos
        angulo_actual = bezier(t, angulo_inicio, angulo_inicio + 10, angulo_fin - 10, angulo_fin)
        duty_cycle = int(ciclo_min + (angulo_actual / 180) * (ciclo_max - ciclo_min))
        pwm.duty_cycle = min(max(duty_cycle, ciclo_min), ciclo_max)
        time.sleep(duracion / pasos)

def posicion_inicial():
    mover_servo_suave(servo_hombro, 90, 90)
    mover_servo_suave(servo_codo, 120, 120)
    mover_servo_suave(servo_base, 90, 90)
    time.sleep(1)  # Espera un segundo después de volver a la posición inicial

def detectar_color():
    try:
        buffer = camara()
        azul_count, rojo_count, verde_count = 0, 0, 0
        for i in range(0, len(buffer), 2):
            rgb565 = (buffer[i] << 8) | buffer[i + 1]
            r = ((rgb565 >> 11) & 0x1F) * 8
            g = ((rgb565 >> 5) & 0x3F) * 4
            b = (rgb565 & 0x1F) * 8
            if b > 50 and b > r and b > g:
                azul_count += 1
            elif r > 140 and r > g + 50 and r > b + 50:
                rojo_count += 1
            elif g > 120 and g > r + 50 and g > b + 50:
                verde_count += 1
        if azul_count > rojo_count and azul_count > verde_count:
            return "azul"
        elif rojo_count > azul_count and rojo_count > verde_count:
            return "rojo"
        elif verde_count > azul_count and verde_count > rojo_count:
            return "verde"
        return None
    except:
        return None

def realizar_movimiento(color):
    print(f"Color detectado: {color}, iniciando movimiento...")

    mover_servo_suave(servo_hombro, 180, 65)  # Baja el hombro al máximo
    mover_servo_suave(servo_codo, 40, 220)  # Extiende más el codo
    
    activar_electroiman()
    
    mover_servo_suave(servo_codo, 220, 190)  # Sube un poco menos el codo al recoger
    mover_servo_suave(servo_hombro, 65, 160)  # Regresa el hombro
    
    desactivar_electroiman()
    
    print("Objeto liberado, regresando a posición inicial...")
    posicion_inicial()

def activar_electroiman():
    electroiman.value = True
    time.sleep(1)

def desactivar_electroiman():
    electroiman.value = False
    time.sleep(1)

# Inicio del bucle
posicion_inicial()
while True:
    for angulo in range(0, 180, 10):  
        mover_servo_suave(servo_base, angulo, angulo)
        time.sleep(1)  # CONFIRMACIÓN ANTES DE DETECTAR COLOR

        tiempo_actual = time.time()

        if angulo not in tiempo_ultima_deteccion or tiempo_actual - tiempo_ultima_deteccion[angulo] >= 20:
            color_detectado_1 = detectar_color()
            time.sleep(0.5)  
            color_detectado_2 = detectar_color()
            time.sleep(0.5)  
            color_detectado_3 = detectar_color()
            
            if color_detectado_1 and color_detectado_1 == color_detectado_2 == color_detectado_3:
                posiciones_detectadas[angulo] = color_detectado_1  # Registrar la detección
                tiempo_ultima_deteccion[angulo] = tiempo_actual  # Registrar el tiempo de detección
                realizar_movimiento(color_detectado_1)

    for angulo in range(180, 0, -10):  
        mover_servo_suave(servo_base, angulo, angulo)
        time.sleep(1)  # CONFIRMACIÓN ANTES DE DETECTAR COLOR

        tiempo_actual = time.time()

        if angulo not in tiempo_ultima_deteccion or tiempo_actual - tiempo_ultima_deteccion[angulo] >= 20:
            color_detectado_1 = detectar_color()
            time.sleep(0.5)  
            color_detectado_2 = detectar_color()
            time.sleep(0.5)  
            color_detectado_3 = detectar_color()
            
            if color_detectado_1 and color_detectado_1 == color_detectado_2 == color_detectado_3:
                posiciones_detectadas[angulo] = color_detectado_1  # Registrar la detección
                tiempo_ultima_deteccion[angulo] = tiempo_actual  # Registrar el tiempo de detección
                realizar_movimiento(color_detectado_1)