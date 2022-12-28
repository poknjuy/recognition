import cv2 as cv
import numpy as np

from function import rec

cap = cv.VideoCapture(0)
ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,1000)
ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT,1000)
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

        img = frame
        imgtemfirst = cv.imread('./train/train2/1.jpg')
        imgtemfirst = cv.cvtColor(imgtemfirst, cv.COLOR_RGB2GRAY)
        imgtemfirst = cv.resize(imgtemfirst, (300,300))
        w0, h0 = imgtemfirst.shape[::-1]
        imgtem = img.copy()
        imgtem = cv.cvtColor(imgtem, cv.COLOR_RGB2GRAY)
        resfirst = cv.matchTemplate(imgtem, imgtemfirst, cv.TM_CCOEFF_NORMED)
        min_val0, max_val0, min_loc0, max_loc0 = cv.minMaxLoc(resfirst)
        top_left0 = max_loc0
        bottom_right0 = (top_left0[0] + w0, top_left0[1] + h0)
        cv.rectangle(imgtem,top_left0, bottom_right0, (0, 0, 255), 2)
        

        img = img[top_left0[1]:top_left0[1]+h0,top_left0[0]:top_left0[0]+w0]
        cv.imshow('firsttem', img)
        rec().searchmax()

        
        # img = cv.resize(img, (390, 390))
        rec().searchnow(img)

        if (img is not None) :
                            
                            imggray = rec().gray(img)
                            imgbinary = rec().binary(imggray)
                            # cv.imshow('imgbinary', imgbinary)
                            
                            imgc = rec().searchcircle(img, imggray)
                            # if (num == 1):
                            rec().maxrange()
                            if(imgc is not None):
                                
                                test = rec().searchoutline(imgc, imgc)
                                imgcl = rec().searchlinepro(imgc, test)
                                if(imgcl is not None):
                                    # print('good')                            
                                    result = rec().calculationuser()
                                    # cv.imwrite('G:/recognition/static/uploads/result.jpg', imgcl)
                                    # rec().loss()
                                    cv.imshow('main', imgcl)
                                # cv.waitKey()
                                else:
                                    print('error:' + str() + ' false no line')
                                    # cv.waitKey()
                            else:
                                print('error:' + str() + ' false no circle')
                                # errorcirlce = errorcirlce + 1
        else:
            print('read file error')
        print(result)
    








    if cv.waitKey(1) == ord('q'):
        break
# 完成所有操作后，释放捕获器
cap.release()
cv.destroyAllWindows()
