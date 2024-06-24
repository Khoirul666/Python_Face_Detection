import cv2

kamera = cv2.VideoCapture('rtsp://192.168.1.37:554/Streaming/Channels/102/')

while True:
    _, frame = kamera.read()
    # cv2.imshow("Kamera",frame)
    # cv2.waitKey(1)

    if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
        cv2.imshow("Kamera", frame)
        cv2.waitKey(1)
    else:
        print("Frame kosong atau memiliki dimensi yang tidak valid")