from tkinter import *
from random import randint

#Global variabls to control
frozen = False
fireworks = False

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb

def SnowScape(canvas):

    canvas.pack()

    # Draw Background Gradient
    for i in range (-10, 520, 10):
        canvas.create_oval(-400, i, 1200, 100+i, fill=_from_rgb((1+int(i/25), 1+int(i/25), 10+int(i/7))), outline='')

    # create two ball objects and animate them
    snowflakes = []
    for i in range(0, 50):
        loc = randint(0, 800)
        h = randint(-10, 450)
        snowflakes.append(Snowflake(canvas, loc, h, loc+7, h+7))

    for flake in range(0, 50):
        snowflakes[flake].move_ball()

    snow = []
    snow2 = []
    for i in range(0, 1000, 50):
        snow.append(i)
        snow2.append(i)
        h = randint(480, 500)
        snow.append(h)
        snow2.append(h+10)
    canvas.create_line(snow, smooth="true", fill='white', width=20)
    canvas.create_line(snow2, smooth="true", fill='white', width=20)
    return canvas


def FWKS(canvas):
    canvas.pack()

    # Draw Background Gradient
    for i in range (-10, 520, 5):
        canvas.create_oval(-400, i, 1200, 100+i, fill=_from_rgb((10+int(i/3), 6+int(i/5),  0)), outline='')

    # create two ball objects and animate them
    fwks = []
    for i in range(0, 3):
        loc = randint(100, 700)
        h = 500
        fwks.append(Firework(canvas, loc, h, loc+7, h+7))

    for flake in range(0, 3):
        fwks[flake].move_ball()

    snow = [0, 450]
    for i in range(0, 1000, 50):
        if randint(0, 10) > 3:
            snow.append(i)
            snow.append(500)
            canvas.create_rectangle(snow, fill='black', width=20)
            h = randint(0, 5)
            snow = [i]
            snow.append(400+20*h)

    return canvas

class Snowflake:
    def __init__(self, canvas, x1, y1, x2, y2, rgb = None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.spd = randint(5, 15)
        self.canvas = canvas
        self.rgb = rgb
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=_from_rgb((150+self.spd*5, 150+self.spd*5, 150+self.spd*5)), outline='')

    def move_ball(self):
        deltax = 0 if frozen else randint(-1,1)/5.0
        deltay = 0 if frozen else self.spd/100.0

        global fireworks
        #loop to top
        self.y1 = self.y1 + deltay
        if  self.y1 >=500:
            deltay = -510
            self.y1 = self.y1 + deltay
            self.spd = randint(5, 15)

        self.canvas.move(self.ball, deltax, deltay)
        if not fireworks:
            self.canvas.after(1, self.move_ball)

    def move_xplosion(self):
        deltax = 0 if frozen else randint(-100,100)/(20-self.spd)
        deltay = 0 if frozen else randint(-90, 90)/(20-self.spd)

        global fireworks
        #loop to top
        grav = 0 if frozen else -0.05
        self.spd = self.spd + grav
        if  self.spd >= 0:
            self.canvas.move(self.ball, deltax, deltay)
            self.canvas.itemconfig(self.ball, fill=_from_rgb(self.rgb))
            if fireworks:
                self.canvas.after(1, self.move_xplosion)
        else:
            self.canvas.delete(self.ball)

class Firework:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.spd = randint(-90, -70)
        self.delay = randint(0, 100)
        self.canvas = canvas
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=_from_rgb((250, 250, 200)), outline='')

    def move_ball(self):
        deltax = 0 if frozen else randint(-1,1)/3.0
        deltay = 0 if frozen else self.spd/100.0

        global fireworks
        #loop to top
        if self.x1 < 50:
            deltax = 400
        elif self.x1 > 850:
            deltax = -400

        if self.delay > 0:
            self.delay = self.delay - 0.1
        else:
            self.x1 = self.x1 + deltax
            self.y1 = self.y1 + deltay
            grav = 0 if frozen else 0.1
            self.spd = self.spd + grav
            if  self.spd >= 0:
                x = explode(self.canvas, self.x1, self.y1)
                self.spd = randint(-90,-70)
                self.delay = randint(50, 100)
                dx = randint(-200, 200)
                self.canvas.move(self.ball, dx, 500-self.y1)
                self.y1 = 500
                self.x1 = self.x1 + dx
            else:
                self.canvas.move(self.ball, deltax, deltay)

        if fireworks:
            self.canvas.after(1, self.move_ball)



class explode:
    def __init__(self, canvas, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 +30
        self.y2 = y1 +30
        self.spd = randint(50, 90)
        self.canvas = canvas
        #self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=_from_rgb((250, 250, 200)), outline='')
        # create two ball objects and animate them
        snowflakes = []
        rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
        for i in range(0, 12):
            snowflakes.append(Snowflake(canvas, self.x1, self.y1, self.x1+7, self.y1+7, rgb=rgb))

        for flake in range(0, 12):
            snowflakes[flake].move_xplosion()





def pause():
    global frozen
    global stop_tim
    frozen = not frozen

    if frozen:
        stop_tim['text'] = 'Play'
    else:
        stop_tim['text'] = 'Pause'

def switch_scrn():
    canvas.delete("all")
    global fireworks
    fireworks = not fireworks
    FWKS(canvas) if fireworks else SnowScape(canvas)


# initialize root Window and canvas
root = Tk()
root.title("Balls")
root.resizable(False,False)

canvas = Canvas(root, width = 800, height = 500)


SnowScape(canvas)
txt = 'Pause'
stop_tim = Button(root, text=txt, command = pause, width=50)
stop_tim.pack(side=LEFT)
switch = Button(root, text='Switch', command = switch_scrn, width = 50)
switch.pack(side=RIGHT)


root.mainloop()
