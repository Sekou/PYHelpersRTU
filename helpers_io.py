#2025, S. Diane

#возвращает короткое имя файла или папки (без пути и расширения)
def get_short_name(file_path):
    pathname, extension = os.path.splitext(file_path)
    return pathname.replace("\\", "/").split('/')[-1]

#возвращает имя папки для заданного файла
def get_dir_name(file_path):
    res = file_path.replace("\\", "/")
    return file_path[:res.rfind("/")]
    
#создает директорию для файла по его пути
def check_create_file_dir(file):
    file_=file.replace("\\", "/")
    dir = file_[:file_.rfind("/")+1]
    os.makedirs(dir, exist_ok=True)
    return dir

#создает директорию по ее пути
def check_create_dir(dir):
    os.makedirs(dir, exist_ok=True)
    return dir

#удаляет директорию 
def remove_dir(dir):
    shutil.rmtree(dir)

#очищает директорию
def clear_dir(dir):
    for root, dirs, files in os.walk(dir):
        for f in files: os.unlink(os.path.join(root, f))
        for d in dirs: shutil.rmtree(os.path.join(root, d))

#спрашивает имя файла
def ask_file():
    import tkinter as tk
    from tkinter import filedialog
    tk.Tk().withdraw()
    return filedialog.askopenfilename(initialdir=".")

#выводит матрицу в 1 строку
def show_mat(mat, prec=5):
    return str([[round(x, prec) for x in r] for r in mat])

#выводит дробное число в округленном формате (например, pad_round(1.2,3,3) = 001.200)
def pad_round(x, p, n): return f"{x:0{1+p+n+(x<0 and 1 or 0)}.{n}f}"

#конверсия многоугольника в строку
def ngon_to_str(pts, prec=3): return "; ".join(f"{round(x,prec):g} {round(y,prec):g}" for x, y in pts)

#конверсия многоугольника из строки
def ngon_from_str(s): return [[float(x[0]),float(x[1])] for x in [xx.split(" ") for xx in s.split("; ")]]

#конверсия массива в строку
def arr_to_str(arr, prec=3): return " ".join(f"{round(x,prec):g}" for x in arr)

#конверсия массива из строки
def arr_from_str(s): return [float(x) for x in s.split(" ")]
