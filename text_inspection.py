#2026, S. Diane, template file for text analysis
import sys, pygame, numpy as np

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)): # отрисовка текста
    screen.blit(pygame.font.SysFont('Courier', sz).render(s, True, с), (x, y))

def draw_multiline_text(screen, text, x, y, sz=25, color=(0,0,0), sep="\n"):
    for i,t in enumerate(text.split(sep)): # отрисовка многострочного текста
        draw_text(screen, t, x, y+sz*i, sz, color)

#разбивает строку на более мелкие строки, чтоб уместить в текстовом поле
def wrap_text(text, width=80):
    lines, ln, ln_sz, index, n = [], "", 0, 0, len(text)
    while index < n:
        if text[start:=index].isspace():# следующий токен - либо слово, либо пробелы
            while index < n and text[index].isspace(): index += 1 # собираем все пробелы
        else: # собираем все слово
            while index < n and not text[index].isspace(): index += 1
        tk = text[start:index]
        if ln_sz + len(tk) <= width: ln, ln_sz = ln + tk, ln_sz + len(tk) # добавл. токен в строку
        else: # если строка не пустая, сохр. её и нач. новую
            if ln: lines.append(ln.lstrip())
            ln, ln_sz = tk, len(tk)
    return "\n".join(lines+[ln] if ln else lines)

def get_word(line, ind):
    i1,i2=ind, ind
    while i1-1>=0 and line[i1-1] not in " ,.!:-?\t": i1-=1
    while i2+1<len(line) and line[i2+1] not in " ,.!:-?\t": i2+=1
    return line[i1:i2+1]

sz = (800, 600)

text="Аннотация – В работе представлен сравнительный анализ современных модификаций метода оптимального предотвращения " \
     "взаимных столкновений (ORCA, Optimal Reciprocal Collision Avoidance), применяемого в качестве локального " \
     "реактивного компонента многоагентных систем маршрутизации мобильных роботов. Рассмотрены фундаментальные " \
     "ограничения реактивной парадигмы ORCA, включая краткосрочный характер планирования, отсутствие учёта " \
     "кинематических ограничений и чувствительность к неопределённости восприятия. Для сопоставления подходов " \
     "предложен унифицированный набор критериев оценки. Проведён анализ современных эволюционных и гибридных " \
     "модификаций ORCA, включая подходы, интегрирующие глобальное планирование и методы глубокого обучения, " \
     "что позволяет расширить область применимости базового метода. Результаты работы показывают, что выбор " \
     "конкретного подхода представляет собой поиск компромисса между расширением функциональности метода и " \
     "сохранением его вычислительной эффективности  с учетом специфики решаемой прикладной задачи."
fragment=fragment=wrap_text(text[:2000])
lines=fragment.split("\n")

pt, ind, ln=[0,0], 0, 0

FONT_SZ=14

x0, y0 = 5, 25
def tr(ln, ind):
    return [x0+0.57*FONT_SZ*ind+0.4*FONT_SZ, y0+1*FONT_SZ*ln+0.6*FONT_SZ]
def untr(x, y):
    return [round((x-x0-0.4*FONT_SZ)/0.57/FONT_SZ), round((y-y0-0.6*FONT_SZ)/1/FONT_SZ)]

if __name__ == "__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                ln,ind=untr(*ev.pos)[::-1]
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    with open("input.txt", "r", encoding="utf-8") as f:
                        text=f.read()
                        fragment=wrap_text(text[:2000])
                        lines=fragment.split("\n")
                if ev.key == pygame.K_w: ln=max(ln-1,0)
                if ev.key == pygame.K_s: ln=min(ln+1,int(sz[1]/0.6/FONT_SZ))
                if ev.key == pygame.K_a: ind=max(ind-1,0)
                if ev.key == pygame.K_d: ind=min(ind+1,int(sz[0]/0.57/FONT_SZ))

        screen.fill((255, 255, 255))

        s=f"Info = ln: {ln} / i: {ind}"
        if len(lines)>ln and ind<len(lines[ln]):
            letter, word = lines[ln][ind], get_word(lines[ln], ind)
            s+=f", \"{letter}\", {word}"
        draw_text(screen, s, 5, 5)
        draw_multiline_text(screen, fragment, 5, 25, sz=FONT_SZ)
        pygame.draw.circle(screen, (255,0,0), tr(ln,ind), 7, 2)

        pygame.display.flip(), timer.tick(fps)
