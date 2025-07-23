#2025, S. Diane

#возвращает короткое имя файла (без пути и расширения)
def get_short_name(file_path):
    pathname, extension = os.path.splitext(file_path)
    return pathname.replace("\\", "/").split('/')[-1]

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
