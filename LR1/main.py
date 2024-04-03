
import tkinter as tk
import math


def validate(a, B):
    if a <= B:
        quit('a не может быть меньше или равно B')


a = float(input('Введите a (a > 0): '))
B = float(input('Введите B (B > 0): '))

validate(a, B)


def zoom(event):
    factor = 1.5 if event.delta > 0 else 0.75
    canvas.scale("all", event.x, event.y, factor, factor)


def start_move(event):
    canvas.scan_mark(event.x, event.y)


def stop_move(event):
    canvas.scan_dragto(event.x, event.y, gain=1)


def draw(canvas, width, height):
    canvas.delete("all")
    w, h = width // 2, height // 2
    # Масштаб
    scale = min(w / B, h / math.sqrt(B ** 3 / (a - B)))
    # Оси
    canvas.create_line(-w, h, width + w, h, fill="black", arrow=tk.LAST)
    canvas.create_line(w, -h, w, height + h, fill="black", arrow=tk.FIRST)
    canvas.create_text(width + w, h + 5, text="OX", fill="black")
    canvas.create_text(w + 5, -h, text="OY", fill="black")
    # Масштабная линейка
    for i in range(-w // int(scale), w // int(scale) + 1):
        if i != 0:
            canvas.create_line(w + i * scale, h - 2, w + i * scale, h + 2, fill="black")
            canvas.create_text(w + i * scale, h + 5, text=str(i), fill="black")
            canvas.create_line(w - 2, h - i * scale, w + 2, h - i * scale, fill="black")
            canvas.create_text(w + 5, h - i * scale, text=str(i), fill="black")
        else:
            canvas.create_text(w - 2, h + 5, text='0', fill="black")
    # График
    for x in range(0, int((B - 0.001) * scale * 1000)):
        x /= 1000
        if x >= a - 0.001:
            break
        y = math.sqrt(x ** 3 / (a - x))
        canvas.create_line(w + x * scale, h - y * scale, w + (x + 0.001) * scale,
                           h - (math.sqrt(((x + 0.001) ** 3) / (a - (x + 0.001))) * scale), fill="blue")
        canvas.create_line(w + x * scale, h + y * scale, w + (x + 0.001) * scale,
                               h + (math.sqrt(((x + 0.001) ** 3) / (a - (x + 0.001))) * scale), fill="blue")


def resize(event):
    draw(canvas, event.width, event.height)


root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=800)
canvas.pack(fill="both", expand=True)

root.bind("<Configure>", resize)
canvas.bind("<MouseWheel>", zoom)
canvas.bind("<ButtonPress-1>", start_move)
canvas.bind("<B1-Motion>", stop_move)
root.mainloop()
