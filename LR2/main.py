import tkinter as tk
import math


def validate(a, H):
    if a <= 0 or H <= 0:
        quit('Сторона и высота не могут быть равны 0.')


a = float(input('Введите размер стороны основания пирамиды: '))
H = float(input('Введите высоту пирамиды: '))

validate(a, H)

vertices = [(0, a, 0),
            (-((0.75 * a ** 2) ** 0.5), a * 0.5, 0),
            (-((0.75 * a ** 2) ** 0.5), -(a * 0.5), 0),
            (0, -a, 0),
            ((0.75 * a ** 2) ** 0.5, -(a * 0.5), 0),
            ((0.75 * a ** 2) ** 0.5, a * 0.5, 0),
            (-((0.1875 * a ** 2) ** 0.5), a * 0.5, H),
            (-((0.75 * a ** 2) ** 0.5), a * 0.25, H),
            (-((0.75 * a ** 2) ** 0.5), -(a * 0.25), H),
            (-((0.1875 * a ** 2) ** 0.5), -(a * 0.5), H),
            (0, -(a * 0.25), H),
            (0, a * 0.25, H)]

edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
         (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 6),
         (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]

global scale_factor
scale_factor = 1.0

faces = [(6, 7, 8, 9, 10, 11),
         (0, 1, 2, 3, 4, 5),
         (0, 1, 7, 6),
         (1, 2, 8, 7),
         (2, 3, 9, 8),
         (3, 4, 10, 9),
         (4, 5, 11, 10),
         (5, 0, 6, 11)]


def draw_pyramid(canvas, width, height):
    canvas.delete("all")
    w, h = width // 2, height // 2
    max_distance = max(math.sqrt(x ** 2 + y ** 2 + z ** 2) for x, y, z in vertices)
    scale = min(w, h) / (2 * max_distance) * scale_factor
    faces_sorted = sorted(faces, key=lambda face: -sum(vertices[i][2] for i in face) / len(face))
    for face in faces_sorted:
        points = [vertices[i] for i in face]
        canvas.create_polygon([(w + x * scale, h - y * scale) for x, y, z in points], fill="purple", outline="black",
                              width=2)


def zoom(event):
    global scale_factor
    scale_factor *= 1.5 if event.delta > 0 else 0.75
    draw_pyramid(canvas, canvas.winfo_width(), canvas.winfo_height())


def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))


def cross_product(v1, v2):
    return (v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0])


def rotation_matrix(axis, theta):
    axis_len = (axis[0] ** 2 + axis[1] ** 2 + axis[2] ** 2) ** 0.5
    axis = (axis[0] / axis_len, axis[1] / axis_len, axis[2] / axis_len)
    a = math.cos(theta / 2.0)
    b, c, d = -axis[0] * math.sin(theta / 2.0), -axis[1] * math.sin(theta / 2.0), -axis[2] * math.sin(theta / 2.0)
    return ((a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)),
            (2 * (b * c + a * d), a * a + c * c - b * b - d * d, 2 * (c * d - a * b)),
            (2 * (b * d - a * c), 2 * (c * d + a * b), a * a + d * d - b * b - c * c))


def rotate_vector(vec, axis, theta):
    rot_matrix = rotation_matrix(axis, theta)
    return (dot_product(rot_matrix[0], vec),
            dot_product(rot_matrix[1], vec),
            dot_product(rot_matrix[2], vec))


def start_move(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y


def stop_move(event):
    global last_x, last_y
    dx, dy = event.x - last_x, event.y - last_y
    for i in range(len(vertices)):
        x, y, z = vertices[i]
        x, y, z = rotate_vector((x, y, z), (0, 1, 0), dx / 10000)
        x, y, z = rotate_vector((x, y, z), (1, 0, 0), dy / 10000)
        vertices[i] = (x, y, z)
    draw_pyramid(canvas, canvas.winfo_width(), canvas.winfo_height())


def resize(event):
    draw_pyramid(canvas, event.width, event.height)


root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=800)
canvas.pack(fill="both", expand=True)

root.bind("<Configure>", resize)
canvas.bind("<MouseWheel>", zoom)
canvas.bind("<ButtonPress-1>", start_move)
canvas.bind("<B1-Motion>", stop_move)

root.mainloop()
