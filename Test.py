import cv2

# Menggunakan URL stream dengan parameter timeout
url = "rtsp://:@192.168.1.37:554/Streaming/Channels/102?timeout=5000"  # timeout dalam milidetik
# kamera = cv2.VideoCapture('rtsp://user:user@192.168.1.37:554/Streaming/Channels/102')


cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Error: Tidak dapat membuka stream.")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Tidak dapat membaca frame dari stream.")
        break
    
    if frame is None or frame.size == 0:
        print("Error: Frame kosong.")
        continue
    
    cv2.imshow("Kamera", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
