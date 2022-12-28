import math

import cv2 as cv
import numpy as np

# import database



def cal_ang(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回任意角的夹角值，这里只是返回点2的夹角
    """
    a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
    b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
    c=math.sqrt(np.int32(np.int32((point_1[0]-point_2[0])*(point_1[0]-point_2[0]))+np.int32((point_1[1]-point_2[1])*(point_1[1] - point_2[1]))))
    A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
    B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
    C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
    # print(a,b,c)
    return B

cap = cv.VideoCapture(0)
# ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,1000)
# ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT,1000)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # 逐帧捕获
    ret, frame = cap.read()
    # 如果正确读取帧，ret为True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # 我们在框架上的操作到这里
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # 显示结果帧e
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('w'):
        # cv.imwrite('frame.jpg', frame)



        file = 'frame.jpg'
        img = cv.imread(file)
        img = cv.resize(img, (900, 480))
        imgtem = imghum = img.copy()
        imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        circles = cv.HoughCircles(imggray, cv.HOUGH_GRADIENT_ALT, 1.5, 50, param1=300, param2=0.8, minRadius=30, maxRadius=0)
        if (circles is not None):
            circles = np.int16(np.around(circles))
            imgc = np.ones([img.shape[0],img.shape[1]])
            circle = np.ones(img.shape, dtype="uint8")
            circle = circle * 255
            cv.circle(circle, (circles[0, 0, 0], circles[0, 0, 1]), circles[0, 0, 2], 0, -1)
            # img = cv.bitwise_or(img, circle)
            # for i in circles[0,:]: #4.5.5.62
            for i in circles: #4.5.3.56
                i = i[0] #4.5.3.56
                cv.circle(circle,(i[0],i[1]),i[2],(0,255,0), 2)
                cv.circle(circle, (i[0],i[1]), 2, (0,0,255), 2)
                cv.circle(img,(i[0],i[1]),i[2],(0,255,0), 2)
                cv.circle(img, (i[0],i[1]), 2, (0,0,255), 2)
                if (i[2] > 170):
                    circletem = i
                elif (i[2] <= 75):
                    circlehum = i
        # cv.imshow('circle', img)
        print(circles)

        mask = np.ones(img.shape, dtype="uint8")
        mask = mask * 255
        # white = mask.copy()
        maskforcenter = mask.copy()
        masktem = mask.copy()
        maskbig = mask.copy()
        # cv.imshow('mask', mask)
        cv.circle(mask, (circlehum[0], circlehum[1]), circlehum[2]-10, 0, -1)
        imghum = cv.bitwise_or(imghum, mask)
        # cv.imshow('imghum', imghum)
        circles = cv.HoughCircles(cv.cvtColor(imghum, cv.COLOR_BGR2GRAY), cv.HOUGH_GRADIENT_ALT, 1, 50, param1=300, param2=0.9, minRadius=0, maxRadius=0)
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv.circle(maskforcenter, (i[0], i[1]), i[2], 0, -1)

        maskforcenter = cv.bitwise_not(maskforcenter)
        # imghum = cv.bitwise_or(imghum, maskforcenter)
        # cv.imshow('maskforcenter', maskforcenter)
        # cv.imshow('imghum', imghum)

        humedge = cv.Canny(imghum, 100, 200)
        humedge = cv.morphologyEx(humedge, cv.MORPH_CLOSE, np.ones((5,5),np.uint8)) 
        kernel = np.ones((3,3),np.uint8)
        humedge = cv.erode(humedge,kernel)
        # humedge = cv.bitwise_not(humedge)
        # humedge = cv.bitwise_or(humedge, cv.cvtColor(mask, cv.COLOR_BGR2GRAY))
        # cv.imshow('humedge', humedge)

        humlines = cv.HoughLinesP(humedge, 1, np.pi/180, 15, minLineLength=circlehum[2]/2, maxLineGap=7)

        white = np.ones(img.shape, dtype="uint8")
        white = white * 255
        if (humlines is not None):
            humlines = np.int16(np.around(humlines))
            for i, cnt in zip(humlines[:],range(10000)):
                if (int((i[0][0] - circlehum[0]) ** 2 + (i[0][1] - circlehum[1]) ** 2) > int((i[0][2] - circlehum[0]) ** 2 + (i[0][3] - circlehum[1]) ** 2)):
                    pointhum = (i[0][0], i[0][1])
                    cv.line(white, (circlehum[0], circlehum[1]), (i[0][0], i[0][1]), (0,0,255), 2)
                    cv.line(imghum, (circlehum[0], circlehum[1]), (i[0][0], i[0][1]), (0,0,255), 2)
                    cv.line(img, (circlehum[0], circlehum[1]), (i[0][0], i[0][1]), (0,0,255), 2)
                else:
                    pointhum = (i[0][2], i[0][3])
                    cv.line(white, (circlehum[0], circlehum[1]), (i[0][2], i[0][3]), (0,0,255), 2)
                    cv.line(imghum, (circlehum[0], circlehum[1]), (i[0][2], i[0][3]), (0,0,255), 2)
                    cv.line(img, (circlehum[0], circlehum[1]), (i[0][2], i[0][3]), (0,0,255), 2)

                # cv.line(white, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0,0,255), 1)
                # cv.line(imghum, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0,0,255), 1)
                # cv.line(white, (circletem[0],circletem[1]), (circlehum[0],circlehum[1]), (0,0,255), 1)
        # cv.imshow('white', white)
        # cv.imshow('imghum', imghum)

        cv.circle(masktem, (circlehum[0], circlehum[1]), circlehum[2] + 15, 0, -1)
        masktem = cv.bitwise_not(masktem)
        imgtem = cv.bitwise_or(imgtem, masktem)
        cv.circle(maskbig, (circletem[0], circletem[1]), circletem[2] - 100, 0, -1)
        imgtem = cv.bitwise_or(imgtem, maskbig)
        # cv.imshow('imgtem', imgtem)

        temedge = cv.Canny(imgtem, 100, 200)
        temedge = cv.morphologyEx(temedge, cv.MORPH_CLOSE, np.ones((5,5),np.uint8)) 
        kernel = np.ones((3,3),np.uint8)
        temedge = cv.erode(temedge,kernel)
        cv.imshow('temedge', temedge)

        temlines = cv.HoughLinesP(temedge, 1, np.pi/180, 30, minLineLength=circletem[2]/9, maxLineGap=0)

        white = np.ones(img.shape, dtype="uint8")
        white = white * 255
        if (temlines is not None):
            temlines = np.int16(np.around(temlines))
            for i, cnt in zip(temlines[:],range(10000)):
                if (int((i[0][0] - circletem[0]) ** 2 + (i[0][1] - circletem[1]) ** 2) > int((i[0][2] - circletem[0]) ** 2 + (i[0][3] - circletem[1]) ** 2)):
                    pointtem = (i[0][0], i[0][1])
                    cv.line(white, (circletem[0], circletem[1]), (i[0][0], i[0][1]), (0,0,255), 2)
                    cv.line(imgtem, (circletem[0], circletem[1]), (i[0][0], i[0][1]), (0,0,255), 2)
                    cv.line(img, (circletem[0], circletem[1]), (i[0][0], i[0][1]), (0,0,255), 2)
                else:
                    pointtem = (i[0][0], i[0][1])
                    cv.line(white, (circletem[0], circletem[1]), (i[0][2], i[0][3]), (0,0,255), 2)
                    cv.line(imgtem, (circletem[0], circletem[1]), (i[0][2], i[0][3]), (0,0,255), 2)
                    cv.line(img, (circletem[0], circletem[1]), (i[0][2], i[0][3]), (0,0,255), 2)

        # cv.imshow('white', white)
        cv.imshow('imgtem', imgtem)

        # cv.line(img, (circletem[0],circletem[1]), (circletem[0],0), (255,0,0),2)
        # cv.line(img, (circlehum[0],circlehum[1]), (circlehum[0],0), (255,0,0),2)
        # # cv.line(img, (circletem[0],circletem[1]), (450, circletem[1]), (255,0,0),2)
        # # cv.line(img, (circlehum[0],circlehum[1]), (450, circlehum[1]), (255,0,0),2)


        humang = cal_ang(pointhum, (circlehum[0], circlehum[1]), (circlehum[0], 0))
        temang = cal_ang(pointtem, (circletem[0], circletem[1]), (circletem[0], 0))
        # print(humang)
        # print(temang)

        if (pointhum[0] > circlehum[0]):
            humdata = humang * 19 / 90 * 2 + 50
        else:
            humdata =50 -  humang * 19 / 90 * 2
        print('humdata:' , humdata)

        if (pointtem[0] > circletem[0]):
            temdata = temang * 29 / 90 * 1 + 17
        else:
            temdata = 17 -  temang * 29 / 90 * 1
        print('temdata:' , temdata)



    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()




# database.insertTempData(temdata +  '')
# database.insertHumData(humdata + '')
# data = "2.3"
# print(data)

# print(circletem, circlehum)
# cv.imshow('', circle)
cv.imshow('origin', img)
cv.waitKey()


 

