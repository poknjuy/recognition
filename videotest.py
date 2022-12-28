import cv2 as cv

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
        cv.imwrite('frame.jpg', frame)
        # delay(1000)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()