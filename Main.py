import face_recognition
import cv2 as cv
import numpy as np
import time
import win32api
import win32con
def opensive(data,angle):#眼睛张开程度
    distance=p=lambda x,y:(x[0]-y[0])**2+(x[1]-y[1])**2
    return (distance(data[1],data[5])+distance(data[2],data[4]))*(1+angle**2)
tan=lambda x,y:(x[1]-y[1])/(x[0]-y[0])#计算偏角
def down():#向下滑动
    for i in range(4):
        win32api.keybd_event(40,0,0,0)# 
        win32api.keybd_event(40,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
        time.sleep(0.2)
def up():#向上滑动
    for i in range(4):
        win32api.keybd_event(38,0,0,0)# 
        win32api.keybd_event(38,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
        time.sleep(0.1)
cap = cv.VideoCapture(0)
t=time.time()
while(True):
    #  一帧一帧的去捕捉视频
    ret, frame = cap.read()
    image = frame
    image=cv.cvtColor(image,cv.COLOR_BGR2GRAY)#转为灰度能加速0.21秒
    face_locations = face_recognition.face_locations(image)
    img =image
    for i in face_locations:
        rectangle= np.zeros(img.shape, np.uint8) #生成一个空灰度图像
        # 矩形左上角和右上角的坐标，绘制一个绿色矩形
        ptLeftTop =(i[3],i[2])
        ptRightBottom =(i[1],i[0])
        point_color = (0, 255, 0) # BGR
        thickness = 1 
        lineType = 4
        cv.rectangle(img, ptLeftTop, ptRightBottom, point_color, thickness, lineType)
    face_landmarks_list = face_recognition.face_landmarks(img)
    p=0
    if len(face_landmarks_list)>=1:
        angle=tan(face_landmarks_list[0]['left_eye'][5],face_landmarks_list[0]['right_eye'][5])
        print('偏移程度',angle)
        if angle<-0.10:
            if time.time()-t>0.01:#间隔时间大于0.01s
                print('下一页！')
                down()
                t=time.time()
        elif angle>0.11:
            if time.time()-t>0.01:#间隔时间大于0.01s
                print('上一页！')
                up()
                t=time.time()
        p=opensive(face_landmarks_list[0]['left_eye'],angle)
        #print('睁眼系数',abs(p))
        
    # 将每帧处理完的图像显示出来
    cv.imshow('frame',image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# 结束之后，释放捕捉，销毁窗口
cap.release()
cv.destroyAllWindows()
