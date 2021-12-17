from tkinter import *
from PIL import Image, ImageDraw
from PIL import ImageTk
from model import infer
from calc import calc

app = Tk()
app.title("Handwriting Calculator with Tensorflow")

WIDTH = 1000
HEIGHT = 300
output_text = StringVar()
visual = StringVar()
visual.set("no")
colors = ["red", "blue", "yellow", "green", "gray", "black", "pink", "purple", "orange", "aqua"]

# canvas设计部分参考了@LogCreative 
# https://github.com/LogCreative/mnist-calculator
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
                         capstyle="round", width=8, fill=fill, tags="inputs")

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
            result = infer(cord2pic(groupedStrokes))
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
                    self.draw_stroke(
                        self.allStrokes[strokeId], colors[(gid - 1) % len(colors)])
        else:
            for stroke in self.allStrokes:
                self.draw_stroke(stroke)

# turn coordinate into 28*28 pixels pictures for model input
def cord2pic(groupedStrokes):
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

    # in case all pixel are in line
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
    output_img = Image.new('L', (a, a), 255)
    output_img.paste(groupimg, ((a-width)//2, (a-height)//2))
    output_img = output_img.resize((28, 28))
    output_img.save("tempImg.jpg")
    return output_img

# Clean the whole screen
def clean_all():
    canvasWriteArea.clean()
    output_text.set("")

# Return to last step
def erase_one(WriteArea):
    # clean last stroke but not the rightest stroke
    if len(WriteArea.seqAllStrokes) <= 0:
        return
    stroke = WriteArea.seqAllStrokes[-1]
    WriteArea.seqAllStrokes.pop()
    WriteArea.allStrokes.remove(stroke)
    groupDict = WriteArea.grouping()
    results = []
    for gid in groupDict.keys():
        groupedStrokes = [WriteArea.allStrokes[sid]
                          for sid in groupDict[gid][0]]
        result = infer(cord2pic(groupedStrokes))
        results.append(result)
    output_text.set(calc(results))
    WriteArea.visualize()

# show the canvas with stroke groups marked


def visualize():
    canvasWriteArea.visualize()


# GUI part
ButtonFrame = Frame(app, borderwidth=2)

canvasWriteArea = WriteArea(
    app, width=WIDTH, height=HEIGHT, bg="white", borderwidth=10)
canvasWriteArea.pack()

result = Label(app, width=60, height=5, bd=10,
               relief=SUNKEN, textvariable=output_text)
result.pack(side=LEFT, fill='y')

selectorGroupIdentify = Checkbutton(ButtonFrame, width=20, height=1, variable=visual,
                                    text="Identify Stroke Groups", onvalue="yes", offvalue="no", command=visualize)
selectorGroupIdentify.pack(side=LEFT)

buttonErase = Button(ButtonFrame, width=12, height=2,
                     text="Clean", relief=RAISED, command=clean_all)
buttonErase.pack(side=LEFT)

buttonReturn = Button(ButtonFrame, width=12, height=2, text="Return",
                      relief=RAISED, command=lambda: erase_one(canvasWriteArea))
buttonReturn.pack(side=RIGHT)

ButtonFrame.pack(side=LEFT, fill=X, ipadx="0.1i", ipady="0.1i", expand=1)
selectorGroupIdentify.pack(side=TOP, padx="0.1i", pady="0.1i")
buttonErase.pack(side=TOP, padx="0.1i", pady="0.1i")
buttonReturn.pack(side=TOP, padx="0.1i", pady="0.1i")

# im=Image.open("tempImg.jpg")
# img=ImageTk.PhotoImage(im)
# imLabel=Label(app,image=img).pack()
# app.update()
# app.after(1000)

label = Label(ButtonFrame)
label.pack(side=TOP)
delay = 10   # in milliseconds

img=None
im=None

def loopCapture():
    im=Image.open("tempImg.jpg")
    img=ImageTk.PhotoImage(im)
    label.config(image=img)
    app.update()
    app.after(delay, loopCapture)
    
loopCapture()

app.mainloop()
