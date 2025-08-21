#S. Diane, expression calculator, 2025

import tkinter as tk
from tkinter import scrolledtext, messagebox
import re

def proc_format():
    input = txt_input_query.get("1.0", tk.END).strip()
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

# запуск приложения
root.mainloop()
