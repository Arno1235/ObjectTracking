import cv2
import numpy as np
import win32api
import pyautogui

state_left = win32api.GetKeyState(0x01)
x1 = 0
y1 = 0
x2 = 0
y2 = 0
yofset = -46

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
ret, originalImage = cap.read()

while True:
    
    a = win32api.GetKeyState(0x01)
    if a != state_left:  # Button state changed
        state_left = a
        if a < 0:
            
            if (x1 == 0 and y1 == 0):
                x1 = pyautogui.position()[0]
                y1 = pyautogui.position()[1] + yofset
            else:
                x2 = pyautogui.position()[0]
                y2 = pyautogui.position()[1] + yofset
    
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    cv2.imshow('Frame', frame)
    
    if (x1 != 0 and y1 != 0 and x2 != 0 and y2 != 0):
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        _, first_frame = cap.read()
        first_frame = cv2.flip(first_frame,1)
        break
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()


trackObj = first_frame[y1: y2, x1: x2]
hsv_trackObj = cv2.cvtColor(trackObj, cv2.COLOR_BGR2HSV)
trackObj_hist = cv2.calcHist([hsv_trackObj], [0], None, [180], [0, 180])
trackObj_hist = cv2.normalize(trackObj_hist, trackObj_hist, 0, 255, cv2.NORM_MINMAX)
term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

x = x1
y = y1
width = x2-x1
height = y2-y1

while True:
    
    cv2.imshow("First Frame", first_frame)
    cv2.imshow("Object", trackObj)
    
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.calcBackProject([hsv], [0], trackObj_hist, [0, 180], 1)
    _, track_window = cv2.meanShift(mask, (x, y, width, height), term_criteria)
    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    