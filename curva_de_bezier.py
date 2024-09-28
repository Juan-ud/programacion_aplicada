import math

# Función para calcular las coordenadas
def calcular_coordenadas(theta, a2, theta1, A3):
    # Convertir ángulos a radianes
    theta_rad = math.radians(theta)
    theta1_rad = math.radians(theta1)
    
    # Calcular x, y (coordenadas del primer brazo)
    x = math.cos(theta_rad) * a2
    y = math.sin(theta_rad) * a2
    
    # Calcular x1, y1 (coordenadas del segundo brazo que se suman a las del primero)
    x1 = x + math.cos(theta1_rad) * A3
    y1 = y + math.sin(theta1_rad) * A3
    
    return x, y, x1, y1

# Valores de ejemplo
theta = 30  # ángulo del primer brazo en grados
a2 = 10     # longitud del primer brazo
theta1 = 45 # ángulo del antebrazo en grados
A3 = 15     # longitud del antebrazo

# Llamar a la función y obtener las coordenadas
x, y, x1, y1 = calcular_coordenadas(theta, a2, theta1, A3)

# Imprimir los resultados
print(f"x=({x}",f"y={y}")
print(f"x1=({x1}",f"y1={y1}")