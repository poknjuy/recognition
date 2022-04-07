import cv2 as cv

from function import rec

class myuse(object):
    def __init__(self):
        self
    def forrec(self, filename):

        train1size = 149
        train2size = 180
        train4size = 10
        errorcirlce = 0
    
        rec().searchmax()
        # for num in range(1, 2):
            # with open('./train/train2/data.txt', "r") as f:
                # for data in f.readlines():
                    # data = data.strip('\n')
                    # data = 6.30
                    # print(data)
                    
        file = filename
        img = cv.imread(file)
        img = cv.resize(img, (390, 390))
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
                                ret = rec().calculationuser()
                                # rec().loss()
                                # cv.imshow('main' + str(num), imgcl)
                            # cv.waitKey()
                            else:
                                print('error:' + str() + ' false no line')
                                # cv.waitKey()
                        else:
                            print('error:' + str() + ' false no circle')
                            errorcirlce = errorcirlce + 1
        else:
                        print('read file error')
        return ret

    # print('errorcirlce:' + str(errorcirlce))
    # rec().searchline(imggray)

    # cv.imwrite('G:/recognition/result.jpg', img)
