import cv2 as cv
import numpy as np

from function import rec

file = './train/train2/' + str(50) + '.jpg'
img = cv.imread(file)
imgresize = cv.resize(img, (390, 390))
cv.imwrite('exmresize.jpg', imgresize)

imggraymax = np.zeros((390, 390))
for i in range(0, 390):
    for j in range(0, 390):
        imggraymax[i][j] = max(imgresize[i][j][0], imgresize[i][j][1], imgresize[i][j][2])
cv.imwrite('exmgraymax.jpg', imggraymax)

imggrayaverage = np.zeros((390, 390))
for i in range(0, 390):
    for j in range(0, 390):
        imggrayaverage[i][j] = (0.333 * imgresize[i][j][0] + 0.333 * imgresize[i][j][1] + 0.333 * imgresize[i][j][2])
cv.imwrite('exmgrayaverage.jpg', imggrayaverage)

imggrayYUV = cv.cvtColor(imgresize, cv.COLOR_BGR2GRAY)
cv.imwrite('exmgrayYUV.jpg', imggrayYUV)

imgblurmedian = cv.medianBlur(imggrayYUV, 5)
cv.imwrite('exmblurmedian.jpg', imgblurmedian)

imgblurgaussian = cv.GaussianBlur(imggrayYUV, (5, 5), 0)
cv.imwrite('exmblurgaussian.jpg', imgblurgaussian)

imgblurbilateral = cv.bilateralFilter(imggrayYUV, 7, 150, 150)
cv.imwrite('exmblurbilateral.jpg', imgblurbilateral)

ret, imgthreshold = cv.threshold(imgblurbilateral, 60, 255, cv.THRESH_BINARY)
cv.imwrite('exmthreshold60.jpg', imgthreshold)

ret, imgthreshold = cv.threshold(imgblurbilateral, 80, 255, cv.THRESH_BINARY)
cv.imwrite('exmthreshold80.jpg', imgthreshold)

imgadaptivethreshold = cv.adaptiveThreshold(imgblurbilateral, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 7, 0.01)
cv.imwrite('exmadaptivethreshold.jpg', imgadaptivethreshold)

imgcanny = cv.Canny(imgblurbilateral, 20, 40)
cv.imwrite('exmcanny.jpg', imgcanny)

imgclosing = cv.morphologyEx(imgcanny, cv.MORPH_CLOSE, (999,999))
cv.imwrite('exmclosing.jpg', imgclosing)

# imgclosing = cv.bitwise_not(imgadaptivethreshold)
# cv.imwrite('filename.jpg', imgclosing)
# imgclosing = cv.morphologyEx(imgclosing, cv.MORPH_OPEN, (999,999))
# imgclosing = cv.bitwise_not(imgclosing)
# cv.imwrite('exmclosing.jpg', imgclosing)

filechapter3 = './train/train2/' + str(7) + '.jpg'
imgchapter3 = cv.imread(filechapter3)
imgresize3 = cv.resize(imgchapter3, (390, 390))
imggrayYUV3 = cv.cvtColor(imgresize3, cv.COLOR_BGR2GRAY)
rec().searchmax()
rec().searchnow(imgresize3)

imgcircle = rec().searchcircle(imgresize3, imggrayYUV3)
cv.imwrite('exmcircle.jpg', imgcircle)

rec().maxrange()

imgoutline = rec().searchoutline(imgcircle, imgcircle)
cv.imwrite('exmoutline.jpg', imgoutline)

imgline = rec().searchlinepro(imgcircle, imgoutline)
cv.imwrite('exmline.jpg', imgline)

imgtem0 = cv.imread('./train/train2/templateexm0.jpg')
imgtem0 = cv.cvtColor(imgtem0, cv.COLOR_RGB2GRAY)
w0, h0 = imgtem0.shape[::-1]
imgtem25 = cv.imread('./train/train2/templateexm25.jpg')
imgtem25 = cv.cvtColor(imgtem25, cv.COLOR_RGB2GRAY)
w25, h25 = imgtem25.shape[::-1]
imgtem = imgchapter3.copy()
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
mid = [imgtem.shape[1]//2,imgtem.shape[0]//2]
cv.line(imgtem, pointmin, mid, (0, 0, 255),2)
cv.line(imgtem, pointmax, mid, (0, 0, 255),2)
cv.imshow('template', imgtem)
cv.imwrite('exmtemplate.jpg', imgtem)