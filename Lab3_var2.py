import numpy as np
import matplotlib.pyplot as plt

# Входные данные
xmin, xmax, ymin, ymax = 0, 8, 0, 6
A = np.array([-5, 10])
B = np.array([1, 1])

# Функция для проверки положения точки относительно окна
def compute_outcode(x, y, xmin, xmax, ymin, ymax):
    code = 0b0000
    if x < xmin: code |= 0b0001
    elif x > xmax: code |= 0b0010
    if y < ymin: code |= 0b0100
    elif y > ymax: code |= 0b1000
    return code

# Алгоритм Коэна-Сазерленда для отсечения отрезка
def cohen_sutherland_clip(A, B, xmin, xmax, ymin, ymax):
    x1, y1 = A
    x2, y2 = B
    outcode1 = compute_outcode(x1, y1, xmin, xmax, ymin, ymax)
    outcode2 = compute_outcode(x2, y2, xmin, xmax, ymin, ymax)
    accept = False

    while True:
        if not (outcode1 | outcode2):
            accept = True
            break
        elif outcode1 & outcode2:
            break
        else:
            x, y = 0, 0
            outcodeOut = outcode1 if outcode1 else outcode2
            if outcodeOut & 0b1000:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif outcodeOut & 0b0100:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif outcodeOut & 0b0010:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif outcodeOut & 0b0001:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin
            if outcodeOut == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, xmax, ymin, ymax)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, xmin, xmax, ymin, ymax)

    if accept:
        return np.array([[x1, y1], [x2, y2]])
    else:
        return None

# Вызов функции отсечения для отрезка AB
clipped_line = cohen_sutherland_clip(A, B, xmin, xmax, ymin, ymax)

# Визуализация
plt.figure()
plt.plot([A[0], B[0]], [A[1], B[1]], 'r-', label='Original Line')
if clipped_line is not None:
    plt.plot(clipped_line[:, 0], clipped_line[:, 1], 'g-', linewidth=2, label='Clipped Line')
plt.plot([xmin, xmin], [ymin, ymax], 'k--')
plt.plot([xmax, xmax], [ymin, ymax], 'k--')
plt.plot([xmin, xmax], [ymin, ymin], 'k--')
plt.plot([xmin, xmax], [ymax, ymax], 'k--')
plt.xlim(-10, 10)
plt.ylim(-10, 15)
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Line Clipping')
plt.grid(True)
plt.show()
