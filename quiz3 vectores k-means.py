import numpy as np

def k_means(vectores, k, max_iter=100):
    vectores = np.array(vectores)
    centroides = vectores[np.random.choice(vectores.shape[0], k, replace=False)]
    for _ in range(max_iter):
        etiquetas = np.argmin(np.linalg.norm(vectores[:, np.newaxis] - centroides, axis=2), axis=1)
        nuevos_centroides = []
        for i in range(k):
            puntos = vectores[etiquetas == i]
            if len(puntos) > 0:
                nuevos_centroides.append(puntos.mean(axis=0))
            else:
                nuevos_centroides.append(centroides[i])
        nuevos_centroides = np.array(nuevos_centroides)
        if np.allclose(centroides, nuevos_centroides):
            break

        centroides = nuevos_centroides

    return etiquetas, centroides
vectores = [
    [4, 2], [2, 1], [3, 9], [8, 3], [3, 9], [10, 10]
]
k = 2
etiquetas, centroides = k_means(vectores, k)

print("Etiquetas:", etiquetas)
print("Centroides finales:", centroides)
