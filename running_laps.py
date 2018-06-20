from tkinter import *
import time
from math import cos, sin, pi


class Runner:

    def __init__(self, canvas, xy, ink, speed, mode):

        self.mode = mode
        self.toggle = False
        self.wave_separation = 60  # delay between waves
        # the scale speed is based on the ratio below. Using 100/6 comes from the scale distance of 100 pixels per mile
        # assuming input speed in minutes per mile, this means each frame represents 10 seconds
        self.laps = 4  # total number of laps to run
        self.buffer = 5.0
        self.theta = 1.57
        self.canvas = canvas
        self.speed = 100 / (6 * speed)
        self.id = self.canvas.create_oval(-3, -3, 3, 3, fill=ink)
        self.label = self.canvas.create_text(xy[0], xy[1], text="     "+str(4-self.laps))  # spaces for legibility
        self.canvas.move(self.id, xy[0], xy[1])

    def __call__(self):
        return self.run

    def run(self):
        xy = self.canvas.coords(self.id)
        if self.mode == 'wave1':
            # run until you get to the circuit
            self.canvas.move(self.id, 0, -self.speed)
            self.canvas.move(self.label, 0, -self.speed)
            if xy[1] < 250:
                self.mode = 'circuit'  # switch to running laps of the circuit
                self.canvas.coords(self.id, 245, 245, 255, 255)
        if self.mode == 'wave2':
            # wait, then move like wave1
            self.wave_separation -= 1
            if self.wave_separation == 0:
                self.mode = 'wave1'
        if self.mode == 'return':
            # run along the straight-away until you get to the finish
            self.canvas.move(self.id, 0, self.speed)
            self.canvas.move(self.label, 0, self.speed)
            if xy[1] > 455:  # based on the coordinate of the bottom of the straight-away
                self.mode = 'stop'  # finish
        if self.mode == 'circuit':
            # run laps around the circuit, count the number of laps, then return to start
            self.canvas.move(self.id, -self.speed * sin(self.theta), self.speed * cos(self.theta))
            self.canvas.move(self.label, -self.speed * sin(self.theta), self.speed * cos(self.theta))

            # mess with the speed coefficient (0.01) to change the circle radius
            self.theta = divmod(self.theta + (0.01 * self.speed), 2 * pi)[1]
            if self.theta < 1 and self.toggle:
                self.laps -= 1
                self.toggle = False
            if self.theta > 1.55 and not self.toggle:
                self.toggle = not self.toggle
                self.canvas.itemconfigure(self.label, text="     "+str(4-self.laps))
            if self.laps == 0 and self.toggle:
                self.mode = 'return'

        # I was trying to make the ovals get big, then fade back as they overtake people. uncomment this to see
        # self.canvas.coords(self.id, xy[0]+self.buffer, xy[1]+self.buffer, xy[2]-self.buffer, xy[3]-self.buffer)

        if len(self.canvas.find_overlapping(xy[0] - 3, xy[1] - 3, xy[0] + 3, xy[1] + 3)) > 1 and self.buffer == 5:
            self.buffer = 25
        if self.buffer > 5:
            self.buffer -= 1

        return self.run


root = Tk()
root.title("Run")
root.resizable(0, 0)
frame = Frame(root, bd=5, relief=SUNKEN)
frame.pack()

canvas = Canvas(frame, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()

# Change runner start coordinates, color, speed (min/mile) and start wave (delay set above, currently 10 scale minutes)
# to start at the bottom of the straigh-away, change the y coordinate to 470
items = [Runner(canvas, (250, 250), "blue", 5, 'wave1'),
         Runner(canvas, (250, 250), "dodger blue", 5.25, 'wave1'),
         Runner(canvas, (250, 250), "sky blue", 6.17, 'wave1'),
         Runner(canvas, (250, 250), "deep pink", 5.5, 'wave2'),
         Runner(canvas, (250, 250), "hot pink", 5.75, 'wave2'),
         Runner(canvas, (250, 250), "pink", 7.25, 'wave2')]

# Change bounding box of the oval. Keep things to scale, like 100 pixels per mile. Radius 95.5 or 127.3 for 6 or 8 miles
circuit = canvas.create_oval(-95.5, -95.5, 95.5, 95.5)
canvas.move(circuit, 250, 150)
bar = canvas.create_line(0, 220, 0, 0)
canvas.move(bar, 250, 245.5)
canvas.create_text(250, 30, text="Mile 3")
canvas.create_text(135, 100, text="Mile 2")
canvas.create_text(365, 100, text="Mile 4")
canvas.create_text(135, 200, text="Mile 1")
canvas.create_text(365, 200, text="Mile 5")
canvas.create_text(250, 470, text="Finish")

root.update()

try:
    while 1:
        for i in range(len(items)):
            items[i] = items[i]()
            root.update_idletasks()
        time.sleep(0.05)
        root.update()
except TclError:
    pass