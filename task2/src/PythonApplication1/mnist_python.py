import clr
SWF = clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WinForms
clr.AddReference("Model")
import Model
from System.Drawing import Size, Point, Bitmap, Graphics, Color, Pen
from System.Drawing.Drawing2D import LineCap
from System import Single, Double
from System.Collections.Generic import List, IEnumerable

import sys
assembly_path = '.\\bin\\x64\\Release'
sys.path.append(assembly_path) #指定.dll文件目录
clr.AddReference("Model")
import Model

class MnistApp(WinForms.Form):
    #设置前端参数

    def __init__(self):
    #设置前端参数 (reference: MainWindow.Designer.cs)
        #设置整体界面
        self.Text = "Handwritten Digit Recognition"
        #self.AutoScaleBaseSize = Size(5, 13)
        self.ClientSize = Size(800, 600)
        self.MinimumSize = Size(800, 600)

        #设置书写区
        self.writeArea = WinForms.PictureBox()
        self.Form_Load()
        self.writeArea.Size = Size(500,500)
        self.writeArea.Location = Point(10, 10)
        self.writeArea.Image = Bitmap(self.writeArea.Width, self.writeArea.Height)
        self.writeArea.MouseDown += self.writeArea_MouseDown
        self.writeArea.MouseMove += self.writeArea_MouseMove
        self.writeArea.MouseUp += self.writeArea_MouseUp 
        self.graphics = Graphics.FromImage(self.writeArea.Image)  
        self.startPoint = Point(0,0) 
        self.ImageSize = 28 #设置图片大小，正确的图片大小对正确率有很大影响

        #设置识别结果
        self.outputText = WinForms.Label()
        self.outputText.Location = Point(600,50)
        self.outputText.Size = Size(100,100)
        
        #设置清除按钮
        self.button = WinForms.Button()
        self.button.Location = Point(550, 400)
        self.button.Size = Size(100, 100)
        #self.button.TabIndex = 2
        self.button.Text = "clear"
        self.button.Click += self.clean_click

        #设置Form
        self.Controls.Add(self.button)
        self.Controls.Add(self.outputText)
        self.Controls.Add(self.writeArea)
        #self.clean_click()
        #一开始清空画板和识别结果
        self.graphics.Clear(Color.White)
        self.writeArea.Invalidate()
        self.outputText.Text = ""
        
        

#加载模型 (reference: MainWindows.cs)  
#学习MainWindows中的函数逻辑，用python语言实现
    def Form_Load(self):
        self.model = Model.Mnist() #引用Mnist类    
        self.writeArea.Image = Bitmap(self.writeArea.Width, self.writeArea.Height)
        #self.graphics = Graphics.FromImage(self.writeArea.Image)

    def clean_click(self, sender, e):
        self.graphics.Clear(Color.White)
        self.writeArea.Invalidate()
        self.outputText.Text = ""
    
    def writeArea_MouseDown(self, sender, e): #这里的参数必须如此，要和WinForm中的函数定义一致
        if e.Button == WinForms.MouseButtons.Left:
            self.startPoint = e.Location
#记录移动轨迹
    def writeArea_MouseMove(self, sender, e):
        if e.Button == WinForms.MouseButtons.Left:
            penStyle = Pen(Color.Black, float(40))
            penStyle.StartCap = LineCap.Round
            penStyle.EndCap = LineCap.Round
            self.graphics.DrawLine(penStyle, self.startPoint, e.Location)
            self.writeArea.Invalidate()
            self.startPoint = e.Location
#抬起鼠标，预测并显示结果
    def writeArea_MouseUp(self, sender, e):
        if e.Button == WinForms.MouseButtons.Left:
            self.outputText.Text = self.pictureHandler()
    
    def pictureHandler(self):
        imageSize = 28
        clonedBmp = Bitmap(self.writeArea.Image, imageSize, imageSize)
        image = List[Single](imageSize * imageSize)
        for i in range(0, imageSize):
            for j in range(0, imageSize):
                color = clonedBmp.GetPixel(j, i)
                average = (color.R + color.G + color.B) /  (3.0)
                oneValue = (average / 255)
                reversed = (0.5 - oneValue)
                image.Add((Single)(reversed))
        input = List[IEnumerable[Single]]()
        input.Add(image)
        inferResult = self.model.Infer(input)
        return self.model.Getoutput(inferResult)


    def run(self):
        WinForms.Application.Run(self)




def main():
    form = MnistApp()
    print ("form created")
    app = WinForms.Application
    print ("app referenced")
    app.Run(form)


if __name__ == "__main__":
    main()