#by Sekou Diane, 2022-2024
import numpy as np
import pygame, sys
import time

WIDTH = 1000
HEIGHT = 800

#расстояние между точками
def dist(p1, p2):
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    return np.sqrt(dx*dx+dy*dy)

#модель объекта
class Obj:
    def __init__(self, x, y, color):
        self.x=x
        self.y=y
        self.color=color
        self.reservedRobot=None #назначенный робот
        self.finished=False #флаг завершенности
    def getPos(self):
        return (self.x, self.y)
    def draw(self, screen):
        r=10
        pygame.draw.ellipse(screen, self.color,
                            [self.x-r, self.y-r, 2*r, 2*r], 2)

#модель робота
class Robot:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.attachedObj=None #прикрепленный объект
        self.target=None #целевая точка
    def getPos(self):
        return (self.x, self.y)
    def draw(self, screen):
        r=20
        pygame.draw.ellipse(screen, (255, 0, 0),
                            [self.x-r, self.y-r, 2*r, 2*r], 2)
    def simulate(self):
        if(self.target!=None):
            p1=self.target
            p2=(self.x, self.y)
            v=np.array(p1)-np.array(p2)
            d=dist(p1, p2) #расстояние от робота до цели
            if(d>0): v=v/d
            self.x+=v[0]*5
            self.y+=v[1]*5
        if(self.attachedObj!=None): #прикреплен ли объект к роботу
            self.attachedObj.x=self.x
            self.attachedObj.y=self.y
    def findNearestObj(self, objs, threshold=100500):
        res=None
        D=100500
        for o in objs:
            if(o.reservedRobot!=None and o.reservedRobot!=self):
                continue
            if(o.finished):
                continue
            dNew=dist(o.getPos(), self.getPos())
            if(dNew<D):
                D=dNew
                res=o
        if(D>threshold):
            res=None
        return res
    def take(self, obj):
        if(obj!=None):
            self.attachedObj=obj

#распределение задач
def distributeTasks(robots, objs, goal):
    #назначение задач каждому из роботов
    for r in robots:
        #проверка окончания транспортировки до целевой точки
        if (r.attachedObj != None and dist(r.getPos(), goal.getPos()) < 20):
            r.attachedObj.finished=True
            r.attachedObj=None #отпускание объекта
            r.target=None
        else:
            #проверка возможности захвата объекта
            if (r.attachedObj == None):
                obj=r.findNearestObj(objs)
                if (obj!=None and dist(r.getPos(), obj.getPos()) < 20):
                    r.take(obj) #захват объекта
                    r.target = goal.getPos()
                    return

        #проверка возможности движения к другим объектам
        if(r.target==None and r.attachedObj==None):
            obj=r.findNearestObj(objs)
            if(obj==None):
                continue
            if(obj.reservedRobot!=None):
                continue
            r.target=obj.getPos()
            obj.reservedRobot=r #фиксация выбора объекта роботом

#критерий окончания алгоритма
def checkMission(robots, objs, goal):
    if all(o.finished for o in objs):
        return True

    if len(robots)==1 and any(o.finished for o in objs):
        return False

    for r in robots:
        if dist(r.getPos(), goal.getPos())>20:
            return False

    for o in objs:
        if o.reservedRobot==None:
            return False

    return True

#создание случайных объектов
def generateObjects(N):
    res=[]
    for i in range(N):
        o=Obj(np.random.randint(50, WIDTH-50),
              np.random.randint(50, HEIGHT-50),
              (0,255,0))
        res.append(o)
    return res

#пример использования
if __name__ == "__main__":

    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))

    start = time.time()

    robots = [
        Robot(150, 150),
        Robot(250, 250),
        Robot(350, 350),
        Robot(390, 300),
        Robot(410, 290),
        Robot(440, 230),
        Robot(480, 250),
        Robot(520, 180),
        Robot(560, 190),
        Robot(600, 220)
        ]

    objs = generateObjects(15)

    goal = Obj(750, 450, (0,0,255))

    #цикл отрисовки
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if(checkMission(robots, objs, goal)):
            break

        screen.fill((255, 255, 255))

        distributeTasks(robots, objs, goal)

        for r in robots:
            r.simulate()
            r.draw(screen)

        for o in objs:
            o.draw(screen)

        goal.draw(screen)

        pygame.display.update()
        pygame.time.delay(50)

    end = time.time()
    print(end - start)
