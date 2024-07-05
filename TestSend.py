import cv2
from ultralytics import YOLO

# Path video file atau URL stream
# video_source = 'rtsp://admin:admin@192.168.1.37:8554/Streaming/Channels/101'
video_source = 'D:\\KHOI\\PYTHON\\Source\\pengendara motor\\video\\VID20240316141158.mp4'
source = "D:\\KHOI\\PYTHON\\Source\\pengendara motor\\video\\selected\\video100216.jpg"

# Membuka video atau gambar
cap = cv2.VideoCapture(video_source)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

# Tentukan ukuran frame output yang diinginkan
output_width = 1280
output_height = 760

# Model YOLO
model = YOLO("D:\\KHOI\\PYTHON\\Coba Python\\Test Detection\\Best.pt")

if not cap.isOpened():
    print("Error: Tidak dapat membuka video.")
else:
    frame_number = 0  # Untuk penamaan gambar hasil crop
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Tidak dapat membaca frame dari stream.")
            break

        if frame is None or frame.size == 0:
            print("Error: Frame kosong.")
            continue
        
        results = model(frame)
        cropped_images = []
        # Dapatkan hasil deteksi
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = f'{model.names[cls]} {conf:.2f}'
                
                # Gambarkan kotak bounding box pada frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                
                # Tambahkan label pada bounding box
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

                # Crop gambar sesuai bounding box
                cropped_image = frame[y1:y2, x1:x2]
                cropped_images.append(cropped_image)

                # Simpan gambar hasil crop
                crop_image_path = f'cropped_image_{frame_number}.jpg'
                # cv2.imwrite(crop_image_path, cropped_image)
                print(f'Gambar hasil crop disimpan di: {crop_image_path}')
                frame_number += 1

        # Ubah ukuran frame
        resized_frame = cv2.resize(frame, (output_width, output_height))

        # Tampilkan frame yang diubah ukurannya
        cv2.imshow('Kamera CCTV', resized_frame)

        # Tampilkan semua gambar hasil crop
        for i, cropped_image in enumerate(cropped_images):
            window_name = f'Cropped Image {i}'
            cv2.imshow(window_name, cropped_image)

        # Tekan 'q' untuk keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release semua resource yang digunakan
    cap.release()
    cv2.destroyAllWindows()
