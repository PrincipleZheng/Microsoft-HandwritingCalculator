from tkinter import *
from typing import Sized
from PIL import ImageGrab, Image, ImageDraw
from colors import getColor
from model import infer
from calc import calc

WIDTH = 1000
HEIGHT = 300

root = Tk()

def constructInput(groupedStrokes):
    # turn coordinate into 28*28 pixels pictures for model input
    groupimg = Image.new('L', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(groupimg)
    SizeData = (WIDTH, HEIGHT, 0, 0)
    
    for stroke in groupedStrokes:
        draw.line(stroke, fill=0, width=10)
        # update the bounding box
        SizeData = (
            min(SizeData[0], min(p[0] for p in stroke)),
            min(SizeData[1], min(p[1] for p in stroke)),
            max(SizeData[2], max(p[0] for p in stroke)),
            max(SizeData[3], max(p[1] for p in stroke))
        )
    
    # this logic is witten in case all pixel are in line
    if SizeData[0] == SizeData[2]:
        SizeData = (
            SizeData[0],
            SizeData[1],
            SizeData[2]+10,
            SizeData[3]
        )
    if SizeData[1] == SizeData[3]:
        SizeData = (
            SizeData[0],
            SizeData[1],
            SizeData[2]+10,
            SizeData[3]
        )
    # print(SizeData)
    groupimg = groupimg.crop(SizeData)
    
    # paste to the new canvas and resize
    width = SizeData[2] - SizeData[0]
    height = SizeData[3] - SizeData[1]

    # to match the training pictures' size (28 * 28 with about 10% margin)
    a = max(width, height) + 60
    exp_img = Image.new('L', (a, a), 255)
    exp_img.paste(groupimg, ((a-width)//2, (a-height)//2))
    exp_img = exp_img.resize((28, 28))
    exp_img.save("img.jpg")
    return exp_img


class WriteArea(Canvas):
    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, kwargs)
        self.bind("<Button-1>", self.mouse_down)
        self.bind("<B1-Motion>", self.paint)
        self.bind("<B1-ButtonRelease>", self.mouse_up)
        self.startPoint = tuple([0, 0])
        self.strokePoints = []
        self.allStrokes = []
        self.seqAllStrokes = []

    def mouse_down(self, event):
        self.startPoint = event.x, event.y
        self.strokePoints.clear()

    def draw_line(self, p1, p2, fill="black"):
        self.create_line(p1[0], p1[1], p2[0], p2[1], joinstyle="round",
                         capstyle="round", width=15, fill=fill, tags="inputs")

    def paint(self, event):
        pos = tuple([event.x, event.y])
        self.draw_line(self.startPoint, pos)
        self.startPoint = pos
        self.strokePoints.append(pos)

    def mouse_up(self, event):
        if len(self.strokePoints) > 0:
            self.allStrokes.append(self.strokePoints.copy())
            self.seqAllStrokes.append(self.strokePoints.copy())
        groupDict = self.grouping()
        results = []
        for gid in groupDict.keys():
            groupedStrokes = [self.allStrokes[sid]
                              for sid in groupDict[gid][0]]
            result = infer(constructInput(groupedStrokes))
            results.append(result)
        output_text.set(calc(results))
        self.visualize()

    def clean(self):
        self.delete("inputs")
        self.allStrokes.clear()

    def draw_stroke(self, stroke, fill="black"):
        prev = stroke[0]
        for _ in range(1, len(stroke)):
            self.draw_line(prev, stroke[_], fill)
            prev = stroke[_]

    def grouping(self):
        """
        return a groupDict:
        [0]: the id's belong to this group
        [1]: the leftend of this group
        [2]: the rightend of this group
        """
        self.allStrokes.sort(key=lambda stroke: min([p[0] for p in stroke]))
        groupDict = {}
        ggid = 0
        for _, stroke in enumerate(self.allStrokes):
            horizontals = [p[0] for p in stroke]
            leftend = min(horizontals)
            rightend = max(horizontals)
            flag = False
            for gid in groupDict.keys():
                if rightend <= groupDict[gid][2] or \
                        groupDict[gid][2] - leftend > (groupDict[gid][2] - groupDict[gid][1]) * 0.1:
                    # contains or mostly overlapped
                    groupDict[gid][0].append(_)
                    # update the edge point
                    groupDict[gid][1] = min(groupDict[gid][1], leftend)
                    groupDict[gid][2] = max(groupDict[gid][2], rightend)
                    flag = True
                    break
            if flag:
                continue
            groupDict[ggid] = [[_], leftend, rightend]
            ggid += 1
        return groupDict

    def visualize(self):
        self.delete("inputs")
        if visual.get() == "yes":
            groupDict = self.grouping()
            for gid in groupDict.keys():
                for strokeId in groupDict[gid][0]:
                    self.draw_stroke(self.allStrokes[strokeId], getColor(gid))
        else:
            for stroke in self.allStrokes:
                self.draw_stroke(stroke)


canvasWriteArea = WriteArea(root, width=WIDTH, height=HEIGHT, bg="white")
canvasWriteArea.pack()

output_text = StringVar()


def clean():
    canvasWriteArea.clean()
    output_text.set("")


buttonErase = Button(root, width=20, height=5, text="Erase", command=clean)
buttonErase.pack(side=LEFT, expand=YES)


def erase_one(WriteArea):
    stroke = WriteArea.seqAllStrokes[-1]
    WriteArea.seqAllStrokes.pop()
    WriteArea.allStrokes.remove(stroke)
    groupDict = WriteArea.grouping()
    results = []
    for gid in groupDict.keys():
        groupedStrokes = [WriteArea.allStrokes[sid]
                          for sid in groupDict[gid][0]]
        result = infer(constructInput(groupedStrokes))
        results.append(result)
    output_text.set(calc(results))
    WriteArea.visualize()

buttonEraseOne = Button(root, width=20, height=5, text="Return",
                        command=lambda: erase_one(canvasWriteArea))
buttonEraseOne.pack(side=RIGHT, expand=YES)

labelResult = Label(root, width=40, height=5, textvariable=output_text)
labelResult.pack()

visual = StringVar()
visual.set("no")


def visualize():
    canvasWriteArea.visualize()


checkbuttonDebug = Checkbutton(root, width=20, height=5, variable=visual,
                               text="Visualize Stroke Groups", onvalue="yes", offvalue="no", command=visualize)
checkbuttonDebug.pack()

root.mainloop()
