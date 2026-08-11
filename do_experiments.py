# 2026, S. Diane
# Example of reading series of experimental plots and values

import matplotlib.pyplot as plt
import os, re, numpy as np

# DIR = "exp"
# DIMS = [10, 3, 4]

DIR = "exp2"
DIMS = [4, 2, 3]

#PART 1 - saving test data

os.makedirs(DIR, exist_ok=True)

def save_plot_and_txt(dir, name, xx, yy, name1="X", name2="Y", color="blue"): # двухмерный график
    plt.plot(xx, yy, color=color), plt.xlabel(name1), plt.ylabel(name2)
    plt.savefig(os.path.join(dir, name)+".png"), plt.close()
    with open(os.path.join(dir, name)+".txt", "w") as f: f.write(f"{yy}")

def experiment(seed, k1, k2): #пример эксперимента
    np.random.seed(seed)
    xx, yy, n, Q = [], [], 1000, 0
    for i in range(n): #основной цикл эксперимента
        y=np.cos(0.01*i+k1)*k2+np.random.normal(0,0.2)
        xx.append(i), yy.append(y)
    Q = np.mean(yy)
    save_plot_and_txt(DIR, f"({seed})-{k1}-{k2}-Q({Q:.7f})", xx, yy)

for seed in range(4):
    experiment(seed,1,1), experiment(seed,1,2), experiment(seed,1,3) #k1=1
    experiment(seed,2,1), experiment(seed,2,2), experiment(seed,2,3) #k1=2

#PART 2 - reading and visualizing

def get_filenames(dir, ext=None): #оперделяет список файлов в папке
    ff = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    if ext is not None: ff = [f for f in ff if f.endswith(ext)]
    return ff

def reshape_list(data, width): # сворачивает список по группам длиной width
    return [data[i: i + width] for i in range(0, len(data), width)]

def compose_files_and_vals(files, dims): #сворачивает линейный список файлов в иерархический список и достает значения
    for d in dims[-1:0:-1]: files=reshape_list(files, d)
    def proc_dim(files):
        if any(isinstance(f, list) for f in files): return [proc_dim(f) for f in files]
        else: return [f.val for f in files]
    return files, proc_dim(files)

def get_plots(files, ik1, ik2): #извлекает набор графиков для определенной под-серии экспериментов
    vv = np.array([f[ik1][ik2].arr for f in files])
    return vv

def show_range_plot(yyy, xx=None): #график стохастической величины с диапазоном
    if xx is None: xx=list(range(len(yyy[0]))) #yyy - список графиков по нескольким экспериментам
    p1,p2,p3 = yyy.min(axis=0), yyy.max(axis=0), yyy.mean(axis=0)
    fill = plt.fill_between(xx, p1, p2, color="#FFEEDD")
    (line,) = plt.plot(xx, p3, color="blue")
    plt.legend([line, fill], ["Среднее", "Диапазон"], loc='upper left')
    plt.show()

class ExperimentFile:
    #e.g.: (0)-1-8-Q(0.0049093).txt - имя в формате (seed)-k1-k2-Q: иерархический номер эксперимента и результат
    def __init__(self, dir, name, num_inds):
        self.name, self.num_inds = name, num_inds
        self.val = float(re.findall(r'\d[\d.]*', name)[-1])
        self.numbers = [float(v) for v in re.findall(r'\d+', name)[:num_inds]]
        with open(os.path.join(dir, name), "r") as f: self.arr=eval(f.read())
    def get_order_ind(self, base=100): #для сортировки
        gg=np.geomspace(1, base**(self.num_inds-1), num=self.num_inds)
        return np.dot(self.numbers, gg[::-1])

files=[ExperimentFile(DIR, f, len(DIMS)) for f in get_filenames(DIR, ".txt")]
files=sorted(files, key=lambda f: f.get_order_ind())
print([f.name for f in files])

files, vals=compose_files_and_vals(files, DIMS)

print("===")
print("MEAN VALUES:")
print(np.mean(vals, axis=0))

# yyy=get_plots(files, 1, 2) #для лучшего значения (индексы определены вручную)
yyy=get_plots(files, 1,1)

show_range_plot(yyy)

# 2026, S. Diane
