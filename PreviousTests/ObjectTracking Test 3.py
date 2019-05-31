import numpy as np
import cv2
import win32api
import pyautogui
import time

state_left = win32api.GetKeyState(0x01)
x1 = 0
y1 = 0
x2 = 0
y2 = 0

cap = cv2.VideoCapture(0)
ret, originalImage = cap.read()
ret, test = cap.read()

#Functies

def mouseControl(a):
    
    global state_left
    global x1
    global x2
    global y1
    global y2
    
    yofset = -46
    
    if cv2.waitKey(1) & 0xFF == ord('r'):
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
    
    if a != state_left:  # Button state changed
        state_left = a
        if a < 0:
            
            if (x1 == 0 and y1 == 0):
                x1 = pyautogui.position()[0]
                y1 = pyautogui.position()[1] + yofset
            else:
                x2 = pyautogui.position()[0]
                y2 = pyautogui.position()[1] + yofset

def frameControl():
    
    global x1
    global x2
    global y1
    global y2
            
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    frame = cv2.flip(frame,1)
    
    if (x1 != 0 and y1 != 0 and x2 != 0 and y2 != 0):
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        
    return frame

def score(imag1, imag2):
    return np.sum(abs(imag1.astype("float") - imag2.astype("float")))



def scoreIma(frame, x, y):
    global x1
    global x2
    global y1
    global y2
    
    xa = int(x1 - ( (x2-x1)/6 ) + x * ( (x2 - x1)/6 ))
    xb = int(xa + x2 - x1)
    ya = int(y1 - ( (y2-y1)/6 ) + y * ( (y2 - y1)/6 ))
    yb = int(ya + y2 - y1)
    
    #print(xb-xa,' , ',yb-ya)
    #print(x2-x1,' , ',y2-y1)
    #print(x,' , ',y)
    
    return frame[ya:yb,xa:xb]

def maakScores(frame, ogIm):
    global x1
    global x2
    global y1
    global y2
    
    punten = np.zeros(shape=(3,3))
    
    for j in range(0,3):
        for i in range(0,3):
            punten[j][i] = score(ogIm,scoreIma(frame,i,j))
            
    print(punten)
    return punten

def laagsteScore(score):
    x = 0
    y = 0
    for j in range(0,3):
        for i in range(0,3):
            if j == 0 and i == 0:
                x = i
                y = j
            else:
                if score[j][i] < score[x][y]:
                    x = i
                    y = j
    
    global x1
    global x2
    global y1
    global y2
    
    xa = int(x1 - ( (x2-x1)/6 ) + x * ( (x2 - x1)/6 ))
    xb = int(xa + x2 - x1)
    ya = int(y1 - ( (y2-y1)/6 ) + y * ( (y2 - y1)/6 ))
    yb = int(ya + y2 - y1)

    return xa, xb, ya, yb

#Main

if __name__ == "__main__":
    
    firstRun = False

    while(True):
        
        mouseControl(win32api.GetKeyState(0x01))
        
        frame = frameControl()
        
        cv2.imshow('frame', frame)
        
        if (x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0):
            
            #frame = frame[y1:y2,x1:x2]
            cv2.imshow('test frame',frame[y1:y2,x1:x2])
            #cv2.imshow('First frame',test)
            
            
            if firstRun == True:
                cv2.imshow('previous image',originalImage)

                scores = maakScores(frame, originalImage)
                x1, x2, y1, y2 = laagsteScore(scores)
                
                cv2.imshow('testje',cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2))
                #time.sleep(0.2)
            else:
                originalImage = np.copy(frame[y1:y2,x1:x2])
                
                firstRun = True
            
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


