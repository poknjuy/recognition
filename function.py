import cmath
import math
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
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT_ALT, 1.5, 100, param1=300, param2=0.55, minRadius=img.shape[0]//4, maxRadius=0) #参数均根据图4微调
        # print(Pointmin)
        if(circles is not None):
            circles = np.uint16(np.around(circles))
            imgc = np.ones([img.shape[0],img.shape[1]])
            circle = np.ones(imgs.shape, dtype="uint8")
            circle = circle * 255
            cv.circle(circle, (circles[0, 0, 0], circles[0, 0, 1]), circles[0, 0, 2], 0, -1)
            imgs = cv.bitwise_or(imgs, circle)
            # cv.imshow(' ', imgs)
            for i in circles[0,:]:
                global circlecenter
                circlecenter = (i[0], i[1])
                cv.circle(imgs,(i[0],i[1]),i[2],(0,255,0), 2)
                cv.circle(imgs, (i[0],i[1]), 2, (0,0,255), 2)
            # cv.imshow('searchcircle', img)
            for i in circles[0,:]:
                cv.circle(imgc,(i[0],i[1]),i[2],(0,255,0), 2)
                cv.circle(imgc, (i[0],i[1]), 2, (0,0,255), 2)
            # cv.imshow('circle', imgc)
            imgtest = imgs.copy()
            cv.line(imgtest, circlecenter, Pointmin, (255, 0, 0), 2)
            # cv.line(imgtest, circlecenter, pointmax, (255, 0, 0), 2)
            cv.imshow('imgtest', imgtest)
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
            global pointline
            if (((lines[0][0][2] - midx) ^ 2 + (lines[0][0][3] - midy) ^ 2) > ((lines[0][0][0] - midx) ^ 2 + (lines[0][0][1] - midy) ^ 2)):
                pointline = (lines[0][0][2], lines[0][0][3])
                cv.line(imgs, circlecenter, (lines[0][0][2], lines[0][0][3]), (0,0,255), 2)
            else:
                pointline = (lines[0][0][0], lines[0][0][1])
                cv.line(imgs, circlecenter, (lines[0][0][0], lines[0][0][1]), (0,0,255), 2)
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
        # cv.drawContours(imgs, contours, -1, (0,255,0), 1)
        
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
        # cv.imshow('return', edgescopy)
        # edges = rec.searchminmax(self, edges)
        # cv.imshow('test', edges)
        

        return edgescopy

    def searchminmax(self, img):
        # cv.imshow('0', img)
        img = cv.dilate(img, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), 5)
        img = cv.erode(img, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), 5)
        cv.imshow('0', img)
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT_ALT, 1.5, 100, param1=300, param2=0.7, minRadius=img.shape[0]//4, maxRadius=0) #参数均根据图4微调
        circles = np.uint16(np.around(circles))
        circle = np.ones(img.shape, dtype="uint8")
        circle = circle * 255
        cv.circle(circle, (circles[0, 0, 0], circles[0, 0, 1]), circles[0, 0, 2] - 9, 0, -1)
        circle = cv.bitwise_not(circle)
        cv.circle(circle, (circles[0, 0, 0], circles[0, 0, 1]), circles[0, 0, 2] - 30, 0, -1)
        
        # circle = cv.bitwise_not(circle)
        img = cv.bitwise_and(img, circle)
        cv.imshow('origin', img)
        # cv.imshow('circle', circle)
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
        lines = cv.HoughLinesP(img, 1, np.pi/180, 10, minLineLength=8)
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
                # cv.line(white, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0,0,255), 2)
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
                        cv.line(white, (midx, midy), (line[0][2], line[0][3]), (0,0,255), 2)
                    else: 
                        print()
                        cv.line(white, (midx, midy), (line[0][0], line[0][1]), (0,0,255), 2)
                    # cv.line(imgs, (lines[0][0][0], lines[0][0][1]), (lines[0][0][2], lines[0][0][3]), (0,0,255), 2)
                else: continue
                # cv.imshow('white', white)
            cv.imshow('white', white)
            return img
        else:
            return None

    def searchmax(self):
        img = cv.imread('./train/train2/1.jpg')
        img = cv.resize(img, (390, 390))
        imgtem0 = cv.imread('./train/train2/template0.jpg')
        imgtem0 = cv.cvtColor(imgtem0, cv.COLOR_RGB2GRAY)
        w0, h0 = imgtem0.shape[::-1]
        imgtem25 = cv.imread('./train/train2/template25.jpg')
        imgtem25 = cv.cvtColor(imgtem25, cv.COLOR_RGB2GRAY)
        w25, h25 = imgtem25.shape[::-1]
        imgtem = img.copy()
        imgtem = cv.cvtColor(imgtem, cv.COLOR_RGB2GRAY)
        res0 = cv.matchTemplate(imgtem, imgtem0, cv.TM_CCOEFF_NORMED)
        min_val0, max_val0, min_loc0, max_loc0 = cv.minMaxLoc(res0)
        top_left0 = max_loc0
        bottom_right0 = (top_left0[0] + w0, top_left0[1] + h0)
        cv.rectangle(imgtem,top_left0, bottom_right0, 255, 2)
        res25 = cv.matchTemplate(imgtem, imgtem25, cv.TM_CCOEFF_NORMED)
        min_val25, max_val25, min_loc25, max_loc25 = cv.minMaxLoc(res25)
        top_left25 = max_loc25
        bottom_right25 = (top_left25[0] + w25, top_left25[1] + h25)
        cv.rectangle(imgtem,top_left25, bottom_right25, 255, 2)
        # cv.line(imgtem, top_left0, bottom_right0, (0, 0, 255))
        
        global pointmin, pointmax
        pointmin = (top_left0[0], top_left0[1]+h0)
        pointmax = (bottom_right25)

        cv.line(imgtem, pointmin, pointmax, (0, 0, 255))
        cv.imshow('template', imgtem)

    def searchnow(self, img):
        imgtem0 = cv.imread('./train/train2/template0.jpg')
        imgtem0 = cv.cvtColor(imgtem0, cv.COLOR_RGB2GRAY)
        w0, h0 = imgtem0.shape[::-1]
        imgtem = img.copy()
        imgtem = cv.cvtColor(imgtem, cv.COLOR_RGB2GRAY)
        res0 = cv.matchTemplate(imgtem, imgtem0, cv.TM_CCOEFF_NORMED)
        min_val0, max_val0, min_loc0, max_loc0 = cv.minMaxLoc(res0)
        top_left0 = max_loc0
        bottom_right0 = (top_left0[0] + w0, top_left0[1] + h0)
        cv.rectangle(imgtem,top_left0, bottom_right0, (0, 0, 255), 2)
        global Pointmin
        Pointmin = (top_left0[0], top_left0[1]+h0)
        cv.imshow('template', imgtem)

    def maxrange(self):
        k1 = (circlecenter[1] - pointmin[1]) / (circlecenter[0] - pointmin[0])
        k2 = (circlecenter[1] - pointmax[1]) / (circlecenter[0] - pointmax[0])
        angletest = abs((k1 - k2) / (1 + k1 * k2))
        angletest = math.atan(angletest)
        angletest = 180 * angletest / math.pi
        global anglemax
        anglemax = 360 - angletest
        # print('anglemax:' + str(anglemax))

    def calculation(self, num):
        print(circlecenter, Pointmin, pointline)
        k1 = (circlecenter[1] - Pointmin[1]) / (circlecenter[0] - Pointmin[0])
        k2 = (circlecenter[1] - pointline[1]) / (circlecenter[0] - pointline[0])
        angletest = abs((k1 - k2) / (1 + k1 * k2))
        angletest = math.atan(angletest)
        angletest = 180 * angletest / math.pi
        global anglenow
        anglenow = angletest
        print('anglenow:' + str(anglenow))
        print('anglemax:' + str(anglemax))
        global ans
        ans = 25 * anglenow / anglemax
        print('ans' + str(num) + ': ' + str(ans))