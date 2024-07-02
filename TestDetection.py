import cv2
from ultralytics import YOLO

# Path video file atau URL stream
# video_source = 'rtsp://admin:admin@192.168.1.37:8554/Streaming/Channels/101'
# video_source = 'D:\\KHOI\\PYTHON\\REF\\pengendara motor\\video\\Suasana Jalan Jatingaleh, Semarang saat jam kerja.mp4'
source = "D:\\KHOI\\PYTHON\\REF\\pengendara motor\\Dataset Plat Nomor\\i25_screenshot-2023-11-30-153007_jpg.rf.f60ac55ffde67a27eb7cd042a9865577.jpg"

# Membuka video
cap = cv2.VideoCapture(source)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

# Tentukan ukuran frame output yang diinginkan
output_width = 640
output_height = 480

#model yolo
model=YOLO("D:\\KHOI\\PYTHON\\Python_Face_Detection\\Detection.pt")

if not cap.isOpened():
    print("Error: Tidak dapat membuka video.")
else:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Tidak dapat membaca frame dari stream.")
            break

        if frame is None or frame.size == 0:
            print("Error: Frame kosong.")
            continue
        
        results = model(frame)
        # Dapatkan hasil deteksi
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                # Gambarkan kotak bounding box pada frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Ubah ukuran frame
        resized_frame = cv2.resize(frame, (output_width, output_height))

        # Tampilkan frame yang diubah ukurannya
        cv2.imshow('Kamera CCTV', resized_frame)

        # Tekan 'q' untuk keluar dari loop
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break

        # Tekan 'q' untuk keluar dari loop
        if cv2.waitKey(10000) & 0xFF == ord('q'):
            break


    # Release semua resource yang digunakan
    cap.release()
    cv2.destroyAllWindows()
