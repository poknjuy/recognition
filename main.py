import cv2 as cv

from function import rec

train1size = 149
train2size = 180
train4size = 10
for num in range(1, 2):
    with open('./train/train2/data.txt', "r") as f:
        # for data in f.readlines():
            # data = data.strip('\n')
            data = 6.30
            print(data)
            file = './train/train2/' + str(num) + '.jpg'
            img = cv.imread(file)
            if (img is not None) :
                imggray = rec().gray(img)
                imgbinary = rec().binary(imggray)
                # cv.imshow('imgbinary', imgbinary)
                
                imgc = rec().searchcircle(img, imggray)
                
                if(imgc is not None):
                    test = rec().searchoutline(imgc, imgc)
                    imgcl = rec().searchlinepro(imgc, test)
                    if(imgcl is not None):
                        print('good')
                        cv.imshow('main' + str(num), imgcl)
                        # cv.waitKey()
                    else:
                        print('error:' + str(num) + ' false no line')
                        # cv.waitKey()
                else:
                    print('error:' + str(num) + ' false no circle')
                    # cv.waitKey()
                # exit()
            else:
                print('read file error')
cv.waitKey()

# rec().searchline(imggray)

# cv.imwrite('G:/recognition/result.jpg', img)
