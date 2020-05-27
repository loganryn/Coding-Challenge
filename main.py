from tkinter import *
from random import randint

#Global variables to control the pausing and which screen to show. They define a basic state machine, with room for additional states to be added.
frozen = False
theme = "snowy"


def _from_rgb(rgb): # https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb


def backgrounds(canvas, theme):
    # Draw Background Gradient
    if theme is "snowy":  #Dark Blue
        for i in range (-10, 520, 10):
            canvas.create_oval(-400, i, 1200, 100+i, fill=_from_rgb((1+int(i/25), 1+int(i/25), 10+int(i/7))), outline='')
    else: #Dusty Orange
        for i in range (-10, 520, 5):
            canvas.create_oval(-400, i, 1200, 100+i, fill=_from_rgb((10+int(i/3), 6+int(i/5),  0)), outline='')

            
def foregrounds(canvas, theme):
    # Create Foreground Texture
    if theme is "snowy": #White Snowfall
        snow = []
        snow2 = []
        for i in range(0, 1000, 50): #traverse the screen width, building a line to define the snow 
            snow.append(i)
            snow2.append(i)
            h = randint(480, 500) #random dips and rises
            snow.append(h)
            snow2.append(h+15)
        canvas.create_line(snow, smooth="true", fill='white', width=20) #create the snowfall line
        canvas.create_line(snow2, smooth="true", fill='white', width=20) #a second layer is needed to cover any background that may show through

    else: # Black Cityscape
        building = [0, 450]
        for i in range(0, 1000, 50): #traverse the screen width, adding buildings one at a time
            if randint(0, 10) > 3: #Add randomness to the building width
                building.append(i)
                building.append(500)
                canvas.create_rectangle(building, fill='black', width=20) #create the building
                h = randint(0, 5)
                building = [i]  #Start the next one adjacent to this one
                building.append(400+20*h)

              
def Landscape(canvas, style, part_system_size, xrange, yrange, part_size):
    #This function sets up the theme and initializes the particle system
    #supported styles: "snowy" & "city"
    backgrounds(canvas, style)
    
    particles = []
    for i in range(0, part_system_size):
        loc = randint(xrange[0], xrange[1]) #Scatter around screen 
        h = randint(yrange[0], yrange[1])
        size = part_size
        if style is "snowy":
            particles.append(Snowflake(canvas, loc, h, loc+size, h+size))
        else: 
            particles.append(Firework(canvas, loc, h, loc+size, h+size))

    for particle in particles:
        particle.update()

    foregrounds(canvas, style)
    return canvas


class Snowflake:
    def __init__(self, canvas, x1, y1, x2, y2, rgb = None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.spd = randint(5, 15) # controlls fall speed and opacity. brighter objects are 'closer' and fall faster 
        self.canvas = canvas
        self.rgb = rgb # controls color if needed
        self.particle = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=_from_rgb((150+self.spd*5, 150+self.spd*5, 150+self.spd*5)), outline='')

    def update(self):
        deltax = 0 if frozen else randint(-1,1)/10.0 #slight swaying 
        deltay = 0 if frozen else self.spd/100.0 #falling

        #recycle snowflake to top of screen
        self.y1 = self.y1 + deltay
        if  self.y1 >=500:
            deltay = -510
            self.y1 = self.y1 + deltay
            self.spd = randint(5, 15)

        self.canvas.move(self.particle, deltax, deltay)
        
        #continue updating if in the snowy theme, otherwise remove objects 
        if theme is "snowy":
            self.canvas.after(1, self.update)
        else:
            self.canvas.delete(self.particle)

    def move_xplosion(self): #recycling the snowflake particles to use for the fireworks explosion
        deltax = 0 if frozen else randint(-100,100)/(20-self.spd) # random cloud
        deltay = 0 if frozen else randint(-90, 90)/(20-self.spd)

        grav = 0 if frozen else -0.05
        self.spd = self.spd + grav
        if  self.spd >= 0: #while the particle has momentum, keep it
            self.canvas.move(self.particle, deltax, deltay)
            self.canvas.itemconfig(self.particle, fill=_from_rgb(self.rgb)) #support color changing
            if theme is "city":
                self.canvas.after(1, self.move_xplosion)
            else: 
                self.canvas.delete(self.particle)
        else: #once it has stopped moving, delete it
            self.canvas.delete(self.particle)

            
class Firework:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.spd = randint(-90, -70)
        self.delay = randint(0, 100)
        self.canvas = canvas
        self.particle = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=_from_rgb((250, 250, 200)), outline='')

    def update(self):
        deltax = 0 if frozen else randint(-1,1)/3.0
        deltay = 0 if frozen else self.spd/100.0

        #if firework is off screen, move it back to the center
        if self.x1 < 50:
            deltax = 400
        elif self.x1 > 850:
            deltax = -400

        if self.delay > 0: #create a random delay between when this firework explodes, and when it respawns 
            self.delay = self.delay - 0.1
        else:
            self.x1 = self.x1 + deltax
            self.y1 = self.y1 + deltay
            grav = 0 if frozen else 0.1
            self.spd = self.spd + grav  #slow down over time (gravity effect)
            if  self.spd >= 0: #once it has reached the peak, explode and recycle after delay 
                x = explode(self.canvas, self.x1, self.y1) #create sub-system for explosion
                self.spd = randint(-90,-70)
                self.delay = randint(50, 100)
                dx = randint(-200, 200)
                self.canvas.move(self.particle, dx, 500-self.y1)
                self.y1 = 500
                self.x1 = self.x1 + dx
            else:
                self.canvas.move(self.particle, deltax, deltay)

        if theme is "city":
            self.canvas.after(1, self.update)
        else:
            self.canvas.delete(self.particle)

         
class explode:
    def __init__(self, canvas, x1, y1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 +30
        self.y2 = y1 +30
        self.spd = randint(50, 90)
        self.canvas = canvas
        
        # use snowflake objects to create the explosion
        snowflakes = []
        rgb = (randint(0, 255), randint(0, 255), randint(0, 255)) #random colors
        for i in range(0, 12): #12 particles per firework
            snowflakes.append(Snowflake(canvas, self.x1, self.y1, self.x1+7, self.y1+7, rgb=rgb))

        for flake in snowflakes:
            flake.move_xplosion()


def pause():
    global frozen
    global stop_time
    frozen = not frozen

    if frozen:
        stop_time['text'] = 'Play'
    else:
        stop_time['text'] = 'Pause'

def switch_screen():
    global theme
    canvas.delete("all") #remove any left over objects
    
    if theme is "snowy": 
        theme = "city"
        Landscape(canvas, style=theme, part_system_size=3, xrange=(100,700), yrange=(500, 500), part_size=5) 
    else: 
        theme = "snowy"
        Landscape(canvas, style=theme, part_system_size=50, xrange=(0,800), yrange=(-10,490), part_size=7)


# initialize root Window and canvas
root = Tk()
root.title("Particle Systems")
root.resizable(False,False)

canvas = Canvas(root, width = 800, height = 500)
canvas.pack()

Landscape(canvas, style=theme, part_system_size=50, xrange=(0,800), yrange=(-10,490), part_size=7)
txt = 'Pause'
stop_time = Button(root, text=txt, command = pause, width=50)
stop_time.pack(side=LEFT)
switch = Button(root, text='Switch', command = switch_screen, width = 50)
switch.pack(side=RIGHT)


root.mainloop()
