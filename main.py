from tkinter import *
from PIL import ImageGrab, Image, ImageDraw
from colors import getColor
from model import infer
from calc import calc

WIDTH = 1000
HEIGHT = 200

root = Tk()

def constructInput(groupedStrokes):
    # Reconstruct the groupedStrokes in a virtual graph
    groupimg = Image.new('L',(WIDTH,HEIGHT),255)
    draw = ImageDraw.Draw(groupimg)
    BB = (WIDTH,HEIGHT,0,0)
    for stroke in groupedStrokes:
        draw.line(stroke,fill=0,width=10)
        # update the bounding box
        BB = (
            min(BB[0], min(p[0] for p in stroke)),
            min(BB[1], min(p[1] for p in stroke)),
            max(BB[2], max(p[0] for p in stroke)),
            max(BB[3], max(p[1] for p in stroke))
            )
    groupimg = groupimg.crop(BB)
    # paste to the new canvas and resize
    w = BB[2] - BB[0]
    h = BB[3] - BB[1]
    # the size of the new image, leave some margin
    a = w + 5 if w > h else h + 5
    exp_img = Image.new('L',(a,a),255)
    exp_img.paste(groupimg, ((a-w)//2,(a-h)//2))
    exp_img = exp_img.resize((28,28))
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

    def mouse_down(self, event):
        self.startPoint = event.x, event.y
        self.strokePoints.clear()

    def draw_line(self, p1, p2, fill="black"):
        self.create_line(p1[0], p1[1], p2[0], p2[1], joinstyle="round", capstyle="round", width=5, fill=fill, tags="inputs")

    def paint(self, event):
        pos = tuple([event.x, event.y])
        self.draw_line(self.startPoint,pos)
        self.startPoint = pos
        self.strokePoints.append(pos)

    def mouse_up(self, event):
        if len(self.strokePoints) > 0:
            self.allStrokes.append(self.strokePoints.copy())
        groupDict = self.grouping()
        results = []
        for gid in groupDict.keys():
            groupedStrokes = [self.allStrokes[sid] for sid in groupDict[gid][0]]
            result = infer(constructInput(groupedStrokes))
            results.append(result)
        output_text.set(calc(results))
        self.visualize()

    def clean(self):
        self.delete("inputs")
        self.allStrokes.clear()

    def draw_stroke(self, stroke, fill="black"):
        prev = stroke[0]
        for _ in range(1,len(stroke)):
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
            if flag: continue
            groupDict[ggid] = [[_], leftend, rightend]
            ggid += 1
        return groupDict

    def visualize(self):
        self.delete("inputs")
        if visual.get() == "yes": 
            groupDict = self.grouping()
            for gid in groupDict.keys():
                for strokeId in groupDict[gid][0]:
                    self.draw_stroke(self.allStrokes[strokeId],getColor(gid))
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
buttonErase.pack()

labelResult = Label(root, width=40, height=5, textvariable=output_text)
labelResult.pack()

visual = StringVar()
visual.set("no")

def visualize():
    canvasWriteArea.visualize()

checkbuttonDebug = Checkbutton(root, width=20, height=5, variable=visual, text="Visualize Stroke Groups", onvalue="yes", offvalue="no", command=visualize)
checkbuttonDebug.pack()

root.mainloop()