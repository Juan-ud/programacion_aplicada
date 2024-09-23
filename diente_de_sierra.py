def onda_diente_sierra(posicionx, frecuencia, amplitud):
    # periodo y la pendiente 
    T = 1 / frecuencia
    
    c_pixeles = T * 512  #todo a pixeles

    # pixeles verticales
    y_amplitud = -6.49 * amplitud + 64

    # pocision por ecuacion de recta 
    posicion = posicionx % c_pixeles

    
    y = (posicion / c_pixeles) * (2 * y_amplitud) - y_amplitud

    return int(y), T

amplitud = 10  
frecuencia = 15
posicionx = 22

# Llamado de la función
y, T = onda_diente_sierra(posicionx, frecuencia, amplitud)
if T > 0:
    print("El periodo calculado es:")
    print(T)
    print("El punto y para la coordenada ingresada es:")
    print(y)
