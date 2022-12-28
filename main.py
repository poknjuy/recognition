import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from function import rec
import time
if __name__ == '__main__':

    
    train1size = 89
    train2size = 180
    train3size = 45
    train4size = 10
    errorcirlce = 0
 
    rec().searchmax()
    sum = 0
    for num in range(7, 8):
        # with open('./train/train1/data.txt', "r") as f:
            # for data in f.readlines():
                # data = data.strip('\n')
                data = 0.625
                # print(data)
                global time_start
                time_start = time.time()
                file = './train/train2/' + str(num) + '.jpg'
                img = cv.imread(file)
                img = cv.resize(img, (390, 390)) #train2 390 390 train3 370 370 train1 320 320
                rec().searchnow(img)


                if (img is not None) :
                    imggray = rec().gray(img)
                    # imggray = rec().bilateralfliter(imggray)
                    imgbinary = rec().binary(imggray)
                    # cv.imwrite('imgbinary.jpg', imgbinary)
                    # cv.imshow('imgbinary', imgbinary)
                    
                    imgc = rec().searchcircle(img, imggray)
                    # cv.imwrite('imgcircle.jpg', imgc)
                    # if (num == 1):
                    rec().maxrange()
                    if(imgc is not None):
                        
                        test = rec().searchoutline(imgc, imgc)
                        # cv.imwrite('imgoutline.jpg', test)
                        imgcl = rec().searchlinepro(imgc, test)
                        # cv.imwrite('imgline.jpg', imgcl)
                        if(imgcl is not None):
                            # print('good')                            
                            ret = rec().calculation(num)
                            # rec().loss(data)
                            cv.imshow('main' + str(num), imgcl)
                            sum = sum+1
                            # cv.imwrite('exmtrain3.jpg', imgcl)
                        # cv.waitKey()
                        else:
                            print('error:' + str(num) + ' false no line')
                            # cv.waitKey()
                    else:
                        print('error:' + str(num) + ' false no circle')
                        errorcirlce = errorcirlce + 1
                else:
                    print('read file error')
                global time_end
                time_end = time.time()
                
                time_sum = time_end - time_start
                # rec().timesum(time_sum)
                # print(time_sum)
    # rec().figure()
    # rec().figuretime()
    
    # print(sum)
    cv.waitKey()

    # print('errorcirlce:' + str(errorcirlce))
    # rec().searchline(imggray)

    # cv.imwrite('G:/recognition/result.jpg', img)
