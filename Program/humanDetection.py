import cv2, serial, psutil
from cvzone.PoseModule import PoseDetector
from guppy import hpy
from time import sleep

psutil.virtual_memory()

# Initial setup
ser = serial.Serial("COM4", 9600)
detector = PoseDetector()
cap = cv2.VideoCapture(0)

h = hpy()
print(h.heap())

last_x = 0
last_y = 0

while True:
    success, frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not success:
        print("Failed to read frame")
        break

    frame = detector.findPose(frame)
    temp, bbox = detector.findPosition(frame)

    if bbox != dict():
        X = 120 - int(bbox.get('center', 0)[0] / (6)) # Subtraction from 120 inverts the direction
        Y = int( (bbox.get('center', 0)[1]) / 6)  # You can change constants to adjust "sensitivity", might fix later
        if abs(X - last_x) >= 2 or abs(Y - last_y) > 1:
            ser.write(str.encode(f"X{X}Y{Y}"))
            print(X, Y)
            last_x = X
            last_y = Y
        

    cv2.imshow("human detection", frame)
 
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print()