#S. Diane, 2026, формирование библиографической записи
import os, tkinter as tk
from tkinter import scrolledtext, messagebox

FOLDER="publications"
STRIP=".: \n/\\"

txt_fields, txt_output=[], None

def clear(): return [t.delete(1.0, tk.END) for t in [*txt_fields, txt_output]]
def open_dir(): os.startfile("publications")
def read(txt_field): return txt_field.get("1.0", tk.END).strip(STRIP)

def save_result():
    if not os.path.exists(FOLDER): os.makedirs(FOLDER)
    with open(f"{FOLDER.strip(STRIP)}/{read(txt_fields[0])}.txt", "w", encoding="utf-8") as f:
        f.write(read(txt_output))

def process():
    ss = [read(t) for t in txt_fields]
    text = f"{ss[0]}. {ss[1]} : {ss[2]} : {ss[3]} : {ss[4]} : {ss[5]} // {ss[6]}. URL: {ss[7]} {ss[8]}."
    txt_output.delete(1.0, tk.END), txt_output.insert(tk.END, text)

def run():
    global txt_fields, txt_output
    (root := tk.Tk()).title("Формирование библиографического описания")

    lines=[ #названия полей и значения по умолчанию
        ["ГОСТ Р *-*:", ""],
        ["Введите заглавие:", ""],
        ["Введите тип:", "нац. стандарт Российской Федерации"],
        ["Введите событие утверждения:", "утвержден и введен в действие Приказом Федерального агентства " +
         "по техническому регулированию и метрологии от ** *** **** г."],
        ["Введите событие введения:", "введен впервые"],
        ["Введите дату введения:", "дата введения ****-**-**"],
        ["Введите название сайта:", "База ГОСТ, ГОСТ Р – национальные стандарты РФ: сайт"],
        ["Введите URL:", "https://rosgosts.ru/file/gost"],
        ["Введите дату обращения:", "(дата обращения: 22.11.2025)"]
    ]

    i=0
    for l in lines: # создаем текстовые поля для ввода короткого названия ГОСТ
        tk.Label(root, text=l[0]).grid(row=i*2, column=0, columnspan=3)
        (tx := tk.Text(root, height=2, width=70)).grid(row=i*2+1, column=0, columnspan=3)
        if len(l[1]): tx.insert(tk.END, l[1])
        txt_fields.append(tx)
        i+=1

    # создаем кнопки и текстовые поля
    btn_convert = tk.Button(root, text="Обработать", command=process).grid(row=i*2, column=0, columnspan=3)
    tk.Label(root, text="Результат: ").grid(row=i*2+1, column=0, columnspan=3)
    (txt_output := tk.Text(root, height=4, width=70)).grid(row=i*2+2, column=0, columnspan=3)
    for j, (name, cmd) in enumerate(zip(["Сохранить", "Откр. папку", "Очистить"], [save_result, open_dir, clear])):
        tk.Button(root, text=name, command=cmd).grid(row=i*2+3, column=j)

    def run(root, name): isinstance(widget:=root.focus_get(), tk.Text) and widget.event_generate(name)
    def keypress(e):# Учет русской раскладки
        for k,s,c in [[86,'v',"Paste"], [67,'c',"Copy"], [88,'x',"Cut"], [65,'a',"SelectAll"]]:
            if e.keycode == k and e.keysym != s: run(root, f"<<{c}>>")
    root.bind("<Control-KeyPress>", keypress)

    root.mainloop() # запуск приложения

if __name__=="__main__": run()
