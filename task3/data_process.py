import cv2
import numpy as np
import random
import os
import imageio


def Noise(image):
    '''
    添加椒盐噪声
    image:原始图片
    prob:噪声比例
    '''

    prob = random.uniform(0.01,0.05) #设置噪点率为随机1%~5%
    output = np.zeros(image.shape,np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            noise_num = random.randint(128, 255) #产生一些灰度稍浅的噪点
            rdn = random.random()#随机生成0-1之间的数字
            if rdn < prob:
                output[i][j] = noise_num
            else:
                output[i][j] = image[i][j]#其他情况像素点不变

    result = output #返回加噪图像
    return result
 

def Rotate(img):    
    height, width = img.shape[:2]    
    angle = 10  
    M = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)    
    return cv2.warpAffine(img, M, (width, height), borderValue=(255, 255, 255))

def ResziePadding(img, fixed_side=28):	

    len = random.randint(14,27) #缩放到50%~100%
    new_w, new_h = len, len 
    resize_img = cv2.resize(img, (new_w, new_h))    # 按比例缩放
    
    # 计算需要填充的像素长度
    if new_w % 2 != 0 and new_h % 2 == 0:
        top, bottom, left, right = (fixed_side - new_h) // 2, (fixed_side - new_h) // 2, (fixed_side - new_w) // 2 + 1, (
            fixed_side - new_w) // 2
    elif new_w % 2 == 0 and new_h % 2 != 0:
        top, bottom, left, right = (fixed_side - new_h) // 2 + 1, (fixed_side - new_h) // 2, (fixed_side - new_w) // 2, (
            fixed_side - new_w) // 2
    elif new_w % 2 == 0 and new_h % 2 == 0:
        top, bottom, left, right = (fixed_side - new_h) // 2, (fixed_side - new_h) // 2, (fixed_side - new_w) // 2, (
            fixed_side - new_w) // 2
    else:
        top, bottom, left, right = (fixed_side - new_h) // 2 + 1, (fixed_side - new_h) // 2, (fixed_side - new_w) // 2 + 1, (
            fixed_side - new_w) // 2

    #print(top, bottom, left, right)
        # 填充图像
    pad_img = cv2.copyMakeBorder(resize_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return pad_img


def main():     
    # cv2.imshow('sp_noise',the_noise)
    # cv2.imshow('sp_noise_img',img_noise)
    # #imageio.imsave("./test.jpg", img_noise)
    # cv2.waitKey(0)
    imageDir = "./)"
    saveDir = "./processed_dataset/rp"
    i = 0

    for name in os.listdir(imageDir):
        #读取一张图片
        i += 1
        imagePath = os.path.join(imageDir,name)
        imageOrigin = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        #缩放
        saveImage = ResziePadding(imageOrigin)
        saveName = "scaled_rp"+str(i)+".png"
        imageio.imsave(os.path.join(saveDir,saveName), saveImage)
        #旋转
        i += 1
        saveImage = Rotate(imageOrigin)
        saveName = "rotated_add"+str(i)+".png"
        imageio.imsave(os.path.join(saveDir,saveName), saveImage)
        #噪点
        i += 1
        saveImage = Noise(imageOrigin)
        saveName = "noise_add"+str(i)+".png"
        imageio.imsave(os.path.join(saveDir,saveName), saveImage)
        #原始
        i += 1
        saveImage = imageOrigin
        saveName = "ori_add"+str(i)+".png"
        imageio.imsave(os.path.join(saveDir,saveName), saveImage)
        #原始
        i += 1
        saveImage = imageOrigin
        saveName = "ori_add"+str(i)+".png"
        imageio.imsave(os.path.join(saveDir,saveName), saveImage)
        #原始
        i += 1
        saveImage = imageOrigin
        saveName = "ori_add"+str(i)+".png"
        imageio.imsave(os.path.join(saveDir,saveName), saveImage)


if __name__ == '__main__':
    main()


