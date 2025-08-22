#S. Diane, expression calculator, 2025

import tkinter as tk
from tkinter import scrolledtext, messagebox
import re

def proc_format():
    input = txt_input.get("1.0", tk.END).strip()
    txt_output.delete(1.0, tk.END)
    if re.fullmatch(r"^[\d+\-*/().]+$", input) is not None:
        res=eval(input)
        txt_output.insert(tk.END, res)

# создаем окно
root = tk.Tk()
root.title("Расчет")
# создаем текстовое поле для ввода названия
lbl_instruct = tk.Label(root, text="Введите выражение:")
lbl_instruct.pack(pady=5)

txt_input = tk.Text(root, height=2, width=70)
txt_input.pack(pady=5)

# создаем кнопку обработки
btn_calc = tk.Button(root, text="Рассчитать", command=proc_format)
btn_calc.pack(pady=5)

# место для вывода результата
lbl_instruct = tk.Label(root, text="Рассчитанный результат: ")
lbl_instruct.pack(pady=5)

txt_output = tk.Text(root, height=2, width=70)
txt_output.pack(pady=5)

# Учет русской раскладки
def run_cmd(root, name):
    if isinstance(widget:=root.focus_get(), tk.Text): widget.event_generate(name)
def keypress(e):
    if e.keycode == 86 and e.keysym != 'v': run_cmd(root, "<<Paste>>")
    elif e.keycode == 67 and e.keysym != 'c': run_cmd(root, "<<Copy>>")
    elif e.keycode == 88 and e.keysym != 'x': run_cmd(root, "<<Cut>>")
    elif e.keycode == 65 and e.keysym != 'a': run_cmd(root, "<<SelectAll>>")
root.bind("<Control-KeyPress>", keypress)

# запуск приложения
root.mainloop()
