import cv2
import pickle
import cvzone
import numpy as kunal

# Use the default camera (0) for capturing live video
cap = cv2.VideoCapture(0)
width, height = 107, 48

def checkParkingSpace(imgpros):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgcrop = imgpros[y:y+height, x:x+width]
        count = cv2.countNonZero(imgcrop)
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1, thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(img, f"Free: {spaceCounter}/{len(posList)}", (100, 50), scale=4, thickness=4, offset=20, colorR=(0, 200, 0))

with open('E:\project car\Venu\CarParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:
    # Read frame from the camera
    success, img = cap.read()
    if not success:
        print("Failed to read from camera")
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernal = kunal.ones((3, 3), kunal.int8)
    imDilate = cv2.dilate(imgMedian, kernal, iterations=1)

    checkParkingSpace(imDilate)
    cv2.imshow("Image", img)

    # Check for exit key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
