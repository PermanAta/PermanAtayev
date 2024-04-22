import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Углы поворота
alpha = np.pi - np.arccos(1/8)
beta = -np.arccos(np.sqrt(7)/4)
gamma = 0  # Угол поворота вокруг оси OZ

# Матрица поворота
def rotation_matrix(alpha, beta, gamma):
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                   [np.sin(gamma), np.cos(gamma), 0],
                   [0, 0, 1]])
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)],
                   [0, 1, 0],
                   [-np.sin(beta), 0, np.cos(beta)]])
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(alpha), -np.sin(alpha)],
                   [0, np.sin(alpha), np.cos(alpha)]])
    return np.dot(Rz, np.dot(Ry, Rx))

# Вершины тетраэдра
vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])

# Применение матрицы поворота
R = rotation_matrix(alpha, beta, gamma)
rotated_vertices = np.dot(vertices, R.T)

# Построение
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Оси
ax.quiver(0, 0, 0, 1, 0, 0, color='r', length=1.2)
ax.quiver(0, 0, 0, 0, 1, 0, color='g', length=1.2)
ax.quiver(0, 0, 0, 0, 0, 1, color='b', length=1.2)

# Тетраэдр
edges = [[rotated_vertices[i], rotated_vertices[j]] for i in range(4) for j in range(i+1, 4)]
collection = Poly3DCollection(edges, linewidths=1, edgecolors='k')
ax.add_collection3d(collection)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
