#2026, S. Diane, реализация одномерного фильтра Калмана
import numpy as np
import matplotlib.pyplot as plt

#Теория по статье: Шестаков А.Л., Келлер А.В. Одномерный фильтр калмана в алгоритмах численного решения задачи оптимального динамического измерения
#https://cyberleninka.ru/article/n/odnomernyy-filtr-kalmana-v-algoritmah-chislennogo-resheniya-zadachi-optimalnogo-dinamicheskogo-izmereniya/

#1
#упрощенный фильтр со статичным коэффициентом доверия
K=0.5 #коэфф. доверия (фильтр доверяет сигналу)
def filter_Kalman_test(yy0):
    res=np.zeros(len(yy0))
    res[0]=yy0[0]
    for i in range(len(yy0)):
        y_=res[max(0,i-1)]
        res[i]=y_ + K*(yy0[i]-y_) #см. формула (10), Шестаков 2021
    return res

#2
#адаптивный фильтр с изменяемым коэффициентом доверия
def get_w(yy0, yy, i, N): #формула (13), Шестаков 2021
    avg_err, w=np.mean([yy0[max(0,i-m)]-yy[max(0,i-m)] for m in range(N)]), 0
    for m in range(N):
        delta=yy0[max(0,i-m)]-yy[max(0,i-m,-1)] - avg_err
        w+=delta**2
    return w / (N-1)

def get_sigma2(yy0, i, N):
    m=np.mean(yy0[max(0,i-N):i+1:1])
    return np.sum((np.array(yy0[max(0,i-N):i+1:1])-m)**2)

def filter_Kalman(yy0):
    yy=np.zeros(len(yy0))
    yy[0]=yy0[0]
    P,P_=0.1,0.1 #задаем небольшие значения чтоб не делить на ноль
    K=0.5 #в местах графика с большим шумом коэф. доверия K будет расти,
    #в стабильных же участках графика будет падать
    for i in range(len(yy)):
        y_=yy[max(0,i-1)]
        P_=P+get_w(yy0, yy, i, N=10)
        sigma2=get_sigma2(yy0, i, N=10)
        if i==0: sigma2=0.01
        K=P_/(P_+sigma2)
        P=(1-K)*P_ #см. формула (14), Шестаков 2021
        yy[i]=y_ + K*(yy0[i]-y_) #см. формула (10), Шестаков 2021
        print(K)
    return yy

np.random.seed(1)

# создание тестовых данных
xx = np.linspace(0, 10 * 2 * np.pi, 1000)
yy = np.sin(xx) + np.random.normal(0, 0.1, 1000)

i=5
length=10
test=yy[i : max(0,i-length): -1]
test2=list(enumerate(test))
print(test2)

# фильтрация
yy1 = filter_Kalman_test(yy)
yy2 = filter_Kalman(yy)

# построение графиков
plt.plot(xx, yy1, label="Kalman static")
plt.plot(xx, yy2, label="Kalman dynamic")

plt.xlabel('x values (radians)')
plt.legend()
plt.title('Sine Wave Plot')
plt.grid(True)
plt.show()
