import cmath
import os

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


class rec(object):
    def __init__(self):
        self

    def gray(self, img):#BGR转灰度
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    def medianfliter(self, img):#中值滤波
        return cv.medianBlur(img, 3)
    
    def bilateralfliter(self, img):#双边滤波
        return cv.bilateralFilter(img, 9, 50, 50)

    def gaussianfliter(self, img):#高斯滤波
        return cv.GaussianBlur(img, (3, 3), 0)

    def binary(self, img):#二值化
        ret, th1 = cv.threshold(img, 100, 255, cv.THRESH_BINARY)
        ret, th2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
        ret, th3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
        ret, th4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
        ret, th5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
        th6 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 999, 0)
        return th1

    def searchcircle(self,imgs,img):#霍夫圆变换 二值化图检测圆不理想 灰度图效果不错仅检测出刻度圆而没有其他干扰
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT_ALT, 1.5, 100, param1=300, param2=0.7, minRadius=img.shape[0]//4, maxRadius=0) #参数均根据图4微调
        if(circles.shape!=0):
            circles = np.uint16(np.around(circles))
            imgc = np.ones([img.shape[0],img.shape[1]])
            circle = np.ones(imgs.shape, dtype="uint8")
            circle = circle * 255
            cv.circle(circle, (circles[0, 0, 0], circles[0, 0, 1]), circles[0, 0, 2], 0, -1)
            imgs = cv.bitwise_or(imgs, circle)
            # cv.imshow(' ', imgs)
            for i in circles[0,:]:
                cv.circle(imgs,(i[0],i[1]),i[2],(0,255,0), 2)
                cv.circle(imgs, (i[0],i[1]), 2, (0,0,255), 2)
            # cv.imshow('searchcircle', img)
            for i in circles[0,:]:
                cv.circle(imgc,(i[0],i[1]),i[2],(0,255,0), 2)
                cv.circle(imgc, (i[0],i[1]), 2, (0,0,255), 2)
            # cv.imshow('circle', imgc)
            return imgs
        else:
            return None

    def searchline(self,imgs,img):#霍夫线变换 canny图 
        edges = cv.Canny(img, 50, 150)
        # cv.imshow('edges', edges)
        lines = cv.HoughLines(edges, 1, np.pi/180, 100) #参数对图3 图4效果均不错
        
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv.line(imgs, (x1, y1), (x2, y2), (0,0,255), 2)
        # cv.imshow('', imgs)
        return imgs
        