#An example of integrating IMU (inertial measurement unit) trajectory, S. Diane, 2025

import numpy as np

def euler_angles_to_rotation_matrix(phi, theta, psi): #Верхний порядок: Z-Y-X (Yaw-Pitch-Roll)
    R_x = np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
    R_y = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    R_z = np.array([[np.cos(psi), -np.sin(psi), 0], [np.sin(psi), np.cos(psi), 0], [0, 0, 1]])
    return R_z @ R_y @ R_x

def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    ang=ang%(2*arc); return ang + (2*arc if ang<-arc else -2*arc if ang>arc else 0)

# Исходные данные (небольшой пример с датчиков телефона Galaxy S20)
data=np.array([ #t ax ay az gx gy gz
[0.0, 0.009, 0.036, 0.05, 0.112, 0.113, 0.119, 0.139, 0.152, 0.169],
[-0.2466, 0.0599, 0.0335, 0.1987, -0.0575, -0.1006, 0.0239, -0.316, -0.5267, -0.6273],
[1.1181, 1.0415, 1.233, 1.1803, 1.3791, 1.3336, 1.0319, 0.9457, 0.996, 0.9074],
[9.886, 9.5029, 9.4023, 9.4957, 9.1869, 9.0624, 9.6034, 9.8907, 9.6657, 9.8285],
[0.0678, 0.0409, -0.1423, -0.0629, -0.0623, -0.0782, -0.1588, -0.1026, -0.1271, -0.1613],
[-0.0531, -0.1662, -0.0806, 0.011, 0.022, 0.0244, -0.0312, 0.0073, 0.0519, 0.0153],
[0.0113, -0.0938, 0.0046, 0.0186, 0.0174, -0.0003, -0.0504, -0.0644, -0.0156, 0.004]])

times, ax_list, ay_list, az_list, gx_list, gy_list, gz_list = data

def find_traj(phi, theta, psi):
    g_earth0=[0, 0, 9.8] # Предполагаем, что изначально датчик вертикален
    velocity = np.zeros(3)
    position = np.zeros(3)
    positions=[[*position]]
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        # Интегрируем углы по гироскопам (предположим, что данные дают углы в рад)
        phi += gx_list[i] * dt
        theta += gy_list[i] * dt
        psi += gz_list[i] * dt
        # Строим матрицу поворота из текущих углов
        R = euler_angles_to_rotation_matrix(phi, theta, psi)
        # Вектор ускорения в локальных осях
        local_accel = np.array([ax_list[i], ay_list[i], az_list[i]])
        # Трансформируем ускорение в глобальную систему
        global_accel = R @ local_accel
        # Трансформируем ускорение свободного падения в глобальную систему
        g_earth = g_earth0
        # Компенсируем (вычитаем) ускорение свободного падения
        global_accel=np.subtract(global_accel, g_earth)
        # Интегрируем ускорение для скорости
        velocity += global_accel * dt
        # Интегрируем скорость для положения
        position += velocity * dt
        positions.append([*position])
    return positions

#метод покоординатного спуска для подбора одного угла Эйлера
def coord_desc_i(angs, i, step=0.05):
    angs_best, traj_best, angs_ = [*angs], find_traj(*angs), [*angs]
    dmin = np.linalg.norm(np.subtract(traj_best[0], traj_best[-1]))
    n=int(np.pi/step); sgn=1
    for st in range(1, n):
        angs_[i] = angs[i]+sgn*st*step
        traj = find_traj(*angs_)
        d = np.linalg.norm(np.subtract(traj[0], traj[-1]))
        if st==1 and d>=dmin:
            sgn=-sgn; angs_[i]+=2*sgn*st*step; traj = find_traj(*angs_)
            d = np.linalg.norm(np.subtract(traj[0], traj[-1]))
        if d < dmin: dmin, angs_best, traj_best = d, [*angs_], traj
        else: break
    return angs_best

#метод покоординатного спуска для подбора всех углов Эйлера
def coord_desc(angs, step=0.05):
    res=[*angs]
    for i in range(len(angs)):
        res=coord_desc_i(res, i, step)
    return res

# Предположим начальные значения углов:
angs_best = (0, 0, 0)
angs_best=coord_desc(angs_best, 0.01) # применим метод покоординатного спуска
angs_best=[lim_ang(a) for a in angs_best]

angs=angs_best
traj_best=find_traj(*angs)

# Выводим результаты
print(f"Число записей: {len(times)}")
print(f"Время: {times[-1]-times[0]} сек")
print(f"Ориентация (рад): phi={angs[0]:.3f}, theta={angs[1]:.3f}, psi={angs[2]:.3f}")
print(f"Положение: {traj_best[-1]}")
print("-" * 50)

def show_traj_3d(traj): # график трехмерной линии
    import matplotlib.pyplot as plt
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.set_xlim(-0.01, 0.01); ax.set_ylim(-0.01, 0.01); ax.set_zlim(-0.01, 0.01)
    ax.plot(*np.swapaxes(traj, 0, 1), label='trajectory')
    ax.legend(); plt.show()

show_traj_3d(traj_best)
