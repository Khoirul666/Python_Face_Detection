import cv2
from ultralytics import YOLO
from io import BytesIO
from telegram import Bot
import numpy as np
import asyncio

# Token bot Telegram
TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''

# Inisialisasi bot Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Path video file atau URL stream
video_source = 'D:\\KHOI\\PYTHON\\Source\\pengendara motor\\video\\selected\\video100216.jpg'

# Membuka video atau gambar
cap = cv2.VideoCapture(video_source)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

# Tentukan ukuran frame output yang diinginkan
output_width = 1280
output_height = 760

# Model YOLO
model = YOLO("D:\\KHOI\\PYTHON\\Coba Python\\Test Detection\\Best.pt")

async def kirim_gambar(cropped_image):
    pass

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
        label_cropped = []
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

                # Crop gambar sesuai bounding box dan masukkan ke dalam array jika label=tidak memakai helm
                cropped_image = frame[y1:y2, x1:x2]
                label_cropped.append(label)
                cropped_images.append(cropped_image)

                # Mengirim gambar hasil crop ke Telegram
                asyncio.run(kirim_gambar(cropped_image))

        # Ubah ukuran frame
        resized_frame = cv2.resize(frame, (output_width, output_height))

        # Tampilkan frame dengan bounding box dan label
        cv2.imshow('Kamera CCTV', resized_frame)

        # Tampilkan semua gambar hasil crop
        for i, cropped_image in enumerate(cropped_images):
            window_name = f'Cropped Image {i}{label_cropped[i]}'
            cv2.imshow(window_name, cropped_image)

        # Tekan 'q' untuk keluar dari loop
        if cv2.waitKey(10000) & 0xFF == ord('q'):
            break

    # Release semua resource yang digunakan
    cap.release()
    cv2.destroyAllWindows()
