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
        ret, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        ret, th2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
        ret, th3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
        ret, th4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
        ret, th5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
        th6 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 999, 0)
        return th1

    def searchcircle(self,imgs,img):#霍夫圆变换 二值化图检测圆不理想 灰度图效果不错仅检测出刻度圆而没有其他干扰
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT_ALT, 1.5, 100, param1=300, param2=0.7, minRadius=img.shape[0]//4, maxRadius=0) #参数均根据图4微调
        if(circles is not None):
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
        # edges = cv.Canny(img, 50, 150)
        # cv.imshow('edges', edges)
        lines = cv.HoughLines(img, 1, np.pi/180, 300)
        i=300
        while(lines==None):
            lines = cv.HoughLines(img, 1, np.pi/180, i) #参数对图3 图4效果均不错
            i=i-1
            if (i < 0): return None
            if(lines is None): continue
            else: break
        if(lines.size != 0):
            test = np.uint16(np.around(lines))
            x = np.mean(lines, axis=0)
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
        else:
            return None
    
    def searchlinepro(self,imgs,img):
        # edges = cv.Canny(img, 50, 150)
        # cv.imshow('', edges)
        # img = cv.Canny(img, 50, 150)
        lines = cv.HoughLinesP(img, 1, np.pi/180, 200, minLineLength=img.shape[0]//10)
        # for line in lines:
        #     cv.line(imgs, (line[0][0],line[0][1]), (line[0][2],line[0][3]), (0,0,255),2)
        i=200
        minlength = img.shape[0]//10
        while(lines is None):
            lines = cv.HoughLinesP(img, 1, np.pi/180, i, minLineLength=minlength) #参数对图3 图4效果均不错
            i=i-1
            if (i < 0):
                minlength = minlength // 2
                i = 200
                continue
            if (minlength <= 10):
                return rec.searchline(self, imgs, img)
                
            if(lines is None): continue
            else: break
            
        if (lines.size != 0):
            midy = img.shape[0]//2
            midx = img.shape[1]//2
            if (((lines[0][0][2] - midx) ^ 2 + (lines[0][0][3] - midy) ^ 2) > ((lines[0][0][0] - midx) ^ 2 + (lines[0][0][1] - midy) ^ 2)):
                cv.line(imgs, (midx, midy), (lines[0][0][2], lines[0][0][3]), (0,0,255), 2)
            else:
                cv.line(imgs, (midx, midy), (lines[0][0][0], lines[0][0][1]), (0,0,255), 2)
            # cv.line(imgs, (lines[0][0][0], lines[0][0][1]), (lines[0][0][2], lines[0][0][3]), (0,0,255), 2)
            return imgs
        else:
            return None
        

    def searchoutline(self,imgs,img):
        edges = cv.Canny(img, 50, 150)
        edgescopy = cv.Canny(img, 50, 150)
        # cv.imshow('', edges)
        edges = cv.dilate(edges, cv.getStructuringElement(cv.MORPH_RECT, (1, 1)), 1)
        
        contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(imgs, contours, -1, (0,255,0), 1)
        
        n = len(contours)
        cv_contours = []
        for contour in contours:
            area = cv.contourArea(contour)
            if area <= 60:
                cv_contours.append(contour)
            else:
                continue
        cv.fillPoly(edges, cv_contours, (255, 0, 0))
        cv.drawContours(edges, cv_contours, -1, (0,255,0), 1)
        edges = cv.erode(edges, cv.getStructuringElement(cv.MORPH_RECT, (1, 1)), 5)
        # edges = cv.ximgproc.thinning(edges, THINNING_ZHANGSUEN)
        # edges = rec.searchline(self, edges, edges)
        cv.imshow('return', edgescopy)
        edges = rec.searchminmax(self, edges)
        cv.imshow('test', edges)
        

        return edgescopy

    def searchminmax(self, img):
        
        img = cv.dilate(img, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), 5)
        img = cv.erode(img, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), 9)
        cv.imshow('origin', img)
        # while(lines==None):
        #     lines = cv.HoughLines(img, 1, np.pi/180, i) #参数对图3 图4效果均不错
        #     i=i-1
        #     if (i < 0): return None
        #     if(lines is None): continue
        #     else: break
        white = np.zeros((img.shape[1], img.shape[0], 3), np.uint8)
        white.fill(255)
        # edges = cv.Canny(img, 50, 150)
        # cv.imshow('', edges)
        # img = cv.Canny(img, 50, 150)
        lines = cv.HoughLinesP(img, 1, np.pi/180, 10, minLineLength=30)
        # for line in lines:
        #     cv.line(imgs, (line[0][0],line[0][1]), (line[0][2],line[0][3]), (0,0,255),2)
        # i=200
        # minlength = img.shape[0]//10
        # while(lines is None):
        #     lines = cv.HoughLinesP(img, 1, np.pi/180, i, minLineLength=minlength) #参数对图3 图4效果均不错
        #     i=i-1
        #     if (i < 0):
        #         minlength = minlength // 2
        #         i = 200
        #         continue
        #     if (minlength <= 10):
        #         return rec.searchline(self, img, img)
                
        #     if(lines is None): continue
        #     else: break
            
        if (lines is not None):
            for line in lines:
                cv.line(white, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0,0,255), 2)
                # cv.imshow('white', white)
                midy = img.shape[0]//2
                midx = img.shape[1]//2
                x1 = line[0][0]
                x2 = line[0][2]
                y1 = line[0][1]
                y2 = line[0][2]
                A = y2 - y1
                B = x1 - x2
                C = x2 * y1 - x1 * y2
                d = (abs(A * midx + B * midy + C)) / (pow((A * A + B * B), 0.5))
                if (d <= 99999):
                    if (((line[0][2] - midx) ^ 2 + (line[0][3] - midy) ^ 2) > ((line[0][0] - midx) ^ 2 + (line[0][1] - midy) ^ 2)):
                        print()
                        # cv.line(white, (midx, midy), (line[0][2], line[0][3]), (0,0,255), 2)
                    else: 
                        print()
                        # cv.line(white, (midx, midy), (line[0][0], line[0][1]), (0,0,255), 2)
                    # cv.line(imgs, (lines[0][0][0], lines[0][0][1]), (lines[0][0][2], lines[0][0][3]), (0,0,255), 2)
                else: continue
                # cv.imshow('white', white)
            cv.imshow('white', white)
            return img
        else:
            return None
