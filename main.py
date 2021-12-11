import cv2 as cv

from function import rec

file = './train/111.jpg'
img = cv.imread(file)
imggray = rec().gray(img)
imgbinary = rec().binary(imggray)
imgc = rec().searchcircle(img, imggray)
if(imgc is not None):
    imgcl = rec().searchline(imgc, imgc)
    if(imgcl is not None):
        cv.imshow('main', imgcl)
        cv.waitKey()
    else:
        print('false no line')
else:
    print('false no circle')
# rec().searchline(imggray)

# cv.imwrite('G:/recognition/result.jpg', img)
