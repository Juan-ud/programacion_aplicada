import numpy as np

def calculo_desplazamiento(Vo, a, T):
    Vo = np.array(Vo)
    a = np.array(a)
    T = np.array(T)
    desplazamiento = Vo * T + 0.5 * a * (T ** 2)

    return desplazamiento
Vo = [0, 0] 
a = [2, 3] 
T = 4 

desplazamiento = calculo_desplazamiento(Vo, a, T)
print("Desplazamiento:", desplazamiento)