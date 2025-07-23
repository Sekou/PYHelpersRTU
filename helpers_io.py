def get_short_name(file_path):
    pathname, extension = os.path.splitext(file_path)
    return pathname.replace("\\", "/").split('/')[-1]

def check_create_file_dir(file):
    file_=file.replace("\\", "/")
    dir = file_[:file_.rfind("/")+1]
    os.makedirs(dir, exist_ok=True)
    return dir

def check_create_dir(dir):
    os.makedirs(dir, exist_ok=True)
    return dir

def remove_dir(dir):
    shutil.rmtree(dir)

def clear_dir(dir):
    for root, dirs, files in os.walk(dir):
        for f in files: os.unlink(os.path.join(root, f))
        for d in dirs: shutil.rmtree(os.path.join(root, d))

def ask_file():
    import tkinter as tk
    from tkinter import filedialog
    tk.Tk().withdraw()
    return filedialog.askopenfilename(initialdir=".")
