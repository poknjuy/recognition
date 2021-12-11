import cv2 as cv

from function import rec

file = 'D:/recognition/train/772.jpg'
img = cv.imread(file)
imggray = rec().gray(img)
imgbinary = rec().binary(imggray)
imgc = rec().searchcircle(img, imggray)
if(imgc.shape!=0):
    imgcl = rec().searchline(imgc, imgc)
    if(imgcl.shape!=0):
        cv.imshow('main', imgcl)
        cv.waitKey()
    else:
        print('false no line')
else:
    print('false no circle')
# rec().searchline(imggray)

# cv.imwrite('G:/recognition/result.jpg', img)
