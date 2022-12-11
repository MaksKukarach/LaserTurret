import cv2, serial, psutil
from cvzone.PoseModule import PoseDetector
from guppy import hpy 

psutil.virtual_memory()
ser = serial.Serial("COM1", 300)
detector = PoseDetector()
cap = cv2.VideoCapture(0)

h = hpy()
print(h.heap())

while True:
    success, frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not success:
        print("Failed to read frame")
        break

    frame = detector.findPose(frame)
    lmlist, bbox = detector.findPosition(frame)

    if bbox != dict():
        Xcoord = 120-int(bbox.get('center', 0)[0]/(640/120))
        Ycoord = int((bbox.get('center', 0)[1]/(480/60)))+45
        ser.write(str.encode(f"X{Xcoord}Y{Ycoord}"))

    cv2.imshow("human detection", frame)
 
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print()