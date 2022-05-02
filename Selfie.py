#Source:https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/?completed=/mog-background-reduction-python-opencv-tutorial/
import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haaracascade_face.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_glasses.xml
eye_cascade = cv2.CascadeClassifier('haaracascade_glasses.xml')



cap = cv2.VideoCapture(0)

#https://learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/

photo_name = input('What would you like the photos image to be? \n(File Extension: .PNG)\nFilename:')
photo_taken = False
idle = False

while cv2.waitKey(30) & 0xff != ord('c'):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    x = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),4)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        roi_text = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        num_eyes = 0
        for (ex,ey,ew,eh) in eyes:
            num_eyes = num_eyes + 1
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'eye',(ex+x,ey+y), font, .4, (30,30,30), 2, cv2.LINE_AA) 
        instructions = ''
        if num_eyes < 2:
            instructions = 'OPEN Both EYES'
        elif num_eyes >=2:
            instructions = 'PHOTO READY, SMILE'
            if not photo_taken and not idle:
                print('Photo:'+photo_name+'.png Saved check directory to get photo')
                photo_taken = True
                ret,frame = cap.read()
                cv2.imwrite(photo_name+'.png',frame)
                response = input('Would you like to take another picture?(Y/N/I => set idle)')
                if response == 'Y':
                    img = input("what is the name of the next image?")
                    photo_name = img
                    photo_taken = False
                elif response == 'N':
                    cap.release()
                    cv2.destroyAllWindows()
                    exit() 
                elif response == 'I':
                    idle = True
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                cap.release()
                cv2.destroyAllWindows()    
        cv2.putText(frame,instructions,(x-20,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,30,0), 2, cv2.LINE_AA) 


    cv2.imshow('frame',frame)
    if cv2.waitKey(30) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()