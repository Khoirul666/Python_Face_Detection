import cv2

# Menggunakan URL stream dengan parameter timeout
url = "rtsp://admin:admin@192.168.1.37:8554/Streaming/Channels/101"  # timeout dalam milidetik

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

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

    # Ubah ukuran frame
    resized_frame = cv2.resize(frame, (640, 320))

    # Tampilkan frame yang diubah ukurannya
    cv2.imshow('Kamera', resized_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
