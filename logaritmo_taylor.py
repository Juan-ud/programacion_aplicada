import math

def fun_log(x, terminos=10):
    if x <= 0:
        return "no puedes usar ese valor "  

    acc = 0        
    u = x - 1      
    signo = 1      # cambiar el signo

    for n in range(1, terminos + 1):
        d = (u ** n) / n  
        
        if abs(d) < 0.001: 
            break
        
        acc += signo * d    #suma o resta segun su signo
        signo *= -1        
    
    return f"ln({x}) ≈ {acc} con {n} términos de la serie de Taylor"


x = 2
terminos = 10   
resultado = fun_log(x, terminos)
print(resultado)
