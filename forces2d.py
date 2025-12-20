import pygame, math, numpy as np

def rot(v, ang): # поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]
def rot_arr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]
def draw_arrow2(screen, color, p0, p1, w): # отрисовка стрелки по 2 точкам
    angle=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)
def draw_rot_rect(screen, color, pc, w, h, ang): #рисует повернутый прямоугольник (по точке центра, ширине, высоте и уголу)
    pygame.draw.polygon(screen, color, np.add(rot_arr([[-w/2, -h/2], [+w/2, -h/2], [+w/2, +h/2], [-w/2, +h/2]], ang), pc), 2)

class Body:
    def __init__(self, rect, density=1):
        self.rect = rect
        self.density = density
        # Положение центра масс
        self.pos = pygame.Vector2(rect.center)
        # Физические свойства
        self.velocity = pygame.Vector2(0, 0)
        self.angular_velocity = 0  # радианы в секунду
        self.angle = 0  # текущий угол в радианах
        # Расчет массы и момента инерции
        self.mass = self.rect.width * self.rect.height * self.density
        # Для прямоугольного сегмента момент инерции относительно центра
        self.moment_of_inertia = (self.mass * (self.rect.width ** 2 + self.rect.height ** 2)) / 12
        # Вектор силы, приложенной к сегменту
        self.force = pygame.Vector2(0, 0)
        # Крутящий момент
        self.torque = 0

    def apply_force(self, force, application_point=None):
        self.force += force
        if application_point is not None:
            # Вектор от центра масс до точки приложения силы
            r = application_point - self.pos
            # Момент силы (крутящий момент)
            torque_from_force = r.cross(force)
            self.torque += torque_from_force

    def update(self, dt):
        # Поступательное движение
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.pos += self.velocity * dt
        # Вращательное движение
        angular_acceleration = self.torque / self.moment_of_inertia
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        # Обновление силы и момента для следующего шага
        self.force = pygame.Vector2(0, 0)
        self.torque = 0

    def draw(self, surface):
        draw_rot_rect(screen, (0,0,0), self.pos, self.rect.width, self.rect.height, self.angle)

# Инициализация pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

p1, p2 = None, None
mousedown=False

fps=20
running = True

# Тестовый объект
body = Body(pygame.Rect(350, 250, 100, 50), 0.001)

while running:
    dt = 1/fps  # Время в секундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.MOUSEMOTION:
            if mousedown: p2 = pygame.Vector2(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p2 = p1 = pygame.Vector2(pygame.mouse.get_pos())
            mousedown=True
        elif event.type == pygame.MOUSEBUTTONUP:
            mousedown=False
            p2 = pygame.Vector2(pygame.mouse.get_pos())
            force_direction = p2 - p1
            force_magnitude = 500  # произвольная сила
            force = force_direction.normalize() * force_magnitude
            # Применим силу к центру или точке вне центра для вращения
            body.apply_force(force, application_point=p1)
            p1, p2 = None, None

    body.update(dt) # Обновление

    screen.fill((255, 255, 255))
    body.draw(screen) # Отрисовка
    if p1 and p2: draw_arrow2(screen, (255,0,0), p1, p2, 2)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

#2025, by S. Diane