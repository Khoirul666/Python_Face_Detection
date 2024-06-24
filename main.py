import cv2

kamera = cv2.VideoCapture('rtsp://192.168.1.37:554/Streaming/Channels/102/')

while True:
    _, frame = kamera.read()
    cv2.imshow("Kamera",frame)
    cv2.waitKey(1)