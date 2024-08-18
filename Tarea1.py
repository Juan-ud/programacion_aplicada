def onda_cuadrada(posicionx, frecuencia, amplitudy):
    # pendiente de al ecuacion 
    m_frecuencia = 0.001953125
    b_frecuencia = 0
    c_pixeles = m_frecuencia * frecuencia * 512 + b_frecuencia

    # Defino la ecuación que relaciona la amplitud con los píxeles verticales
    y_amplitud = -6.49 * amplitudy + 64

   

    # Defino la posición del punto x usando la ecuación de la recta
    posicion = posicionx % c_pixeles

    # miro si esta en el punto positivo o negativo de la onda 
    if posicion < c_pixeles / 2:
        y = y_amplitud
    else:
        y = -y_amplitud

    return int(y), 1 / frecuencia


amplitudy = -10
frecuencia = 15
posicionx = 22

# Llamado de la funcion
y, T = onda_cuadrada(posicionx, frecuencia, amplitudy)
if T>0:
    print("El periodo calculado es:")
    print(T)
    print("El punto y para la coordenada ingresada es:")
    print(y)
    