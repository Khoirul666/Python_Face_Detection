import cv2
from ultralytics import YOLO
from io import BytesIO
from telegram import Bot
import numpy as np

# Token bot Telegram
TELEGRAM_BOT_TOKEN = 'xx'
CHAT_ID = 'xx'

# Inisialisasi bot Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Path video file atau URL stream
video_source = 'D:\\KHOI\\PYTHON\\Source\\pengendara motor\\video\\selected\\video100216.jpg'

# Membuka video atau gambar
cap = cv2.VideoCapture(video_source)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

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

                # Mengirim gambar hasil crop ke Telegram
                image_bytes = cv2.imencode('.jpg', cropped_image)[1].tobytes()
                bio = BytesIO(image_bytes)
                bio.name = 'cropped_image.jpg'
                bio.seek(0)
                bot.send_photo(chat_id=CHAT_ID, photo=bio, caption=label)
                print(f'Gambar hasil crop dikirim ke Telegram.')

        # Tampilkan frame dengan bounding box dan label
        cv2.imshow('Gambar Asli', frame)

        # Tekan 'q' untuk keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release semua resource yang digunakan
    cap.release()
    cv2.destroyAllWindows()
