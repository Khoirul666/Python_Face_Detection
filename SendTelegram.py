import cv2
from ultralytics import YOLO
from io import BytesIO
from telegram import Bot
from telegram.error import TimedOut
import asyncio
import pytesseract
from PIL import Image

# Token bot Telegram
TELEGRAM_BOT_TOKEN = 'xx'
CHAT_ID = 'xx'

# Inisialisasi bot Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Path video file atau URL stream
no_helm = 'D:\\KHOI\\PYTHON\\dataset\\HELM and NO\\PICTURE\\NO HELM\\no_helm 002.jpg'
helm = 'D:\\KHOI\\PYTHON\\dataset\\HELM and NO\\PICTURE\\HELM\\helm 001.jpg'

# Membuka video atau gambar
# cap = cv2.VideoCapture("https://s3.ap-southeast-1.amazonaws.com/moladin.assets/blog/wp-content/uploads/2019/08/15175153/15-Cara-Menjadi-Pengendara-Motor-yang-Baik-di-Jalan-Raya-3.jpg")
cap = cv2.VideoCapture(helm)

cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

# Tentukan ukuran frame output yang diinginkan
output_width = 1280
output_height = 760

# Model YOLO
model = YOLO(r"D:\KHOI\PYTHON\dataset\Detection Helm and Number.v5i.yolov8\best.pt")

async def kirim_gambar(cropped_image,nama_file):
    # while True:
    #     with open(cropped_image,'rb') as image:
    #         await bot.send_photo(chat_id=CHAT_ID, photo=image)
    # pass
    image_bytes = cv2.imencode('.jpg',cropped_image)[1].tobytes()
    bio = BytesIO(image_bytes)
    bio.name = "Gambar Potongan.jpg"
    bio.seek(0)

    # ambil data plat nomor
    skala = 3.0
    c_h = int(cropped_image.shape[0] * skala)
    c_w = int(cropped_image.shape[1] * skala)
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    ri = cv2.resize(cropped_image,(c_w,c_h),interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(ri,cv2.COLOR_BGR2GRAY)
    th,threshold = cv2.threshold(img_gray,100,255,cv2.THRESH_BINARY_INV)
    cv2.imshow(nama_file,threshold)
    # cv2.imshow(cropped_image)
    result = pytesseract.image_to_string((threshold))

    result = ''.join([char for char in result if char.isalnum()])
    count = 3
    for attempt in range(count):
        try:
            # print("isi plat"+result+"isi plat")
            if(result!=''):
                print("isi plat"+result+"isi plat")
                # await bot.send_photo(chat_id=CHAT_ID, photo=bio, caption=result)
            break
        except TimedOut:
            if attempt<count-1:
                await asyncio.sleep(2)
            else:
                raise

async def main():
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
            label_cropped = []
            cropped_images = []
            
            # Dapatkan hasil deteksi
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = f'{model.names[cls]} {conf:.2f}'
                    label1 = f'{model.names[cls]}'
                    
                    # Gambarkan kotak bounding box pada frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    
                    # Tambahkan label pada bounding box
                    cv2.putText(frame, label1, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

                    # Crop gambar sesuai bounding box dan masukkan ke dalam array
                    cropped_image = frame[y1:y2, x1:x2]
                    label_cropped.append(label1)
                    cropped_images.append(cropped_image)

                    # Mengirim gambar hasil crop ke Telegram
                    # print(label1)
                    if(label1=="Pengendara"):
                        await kirim_gambar(cropped_image,label1)

            # Ubah ukuran frame
            resized_frame = cv2.resize(frame, (output_width, output_height))

            # Tampilkan frame dengan bounding box dan label
            cv2.imshow('Kamera CCTV', resized_frame)

            # Tampilkan semua gambar hasil crop
            for i, cropped_image in enumerate(cropped_images):
                window_name = f'{label_cropped[i]}'
                # cv2.imshow(window_name, cropped_image)

            # Tekan 'q' untuk keluar dari loop
            if cv2.waitKey(50000) & 0xFF == ord('q'):
                break

        # Release semua resource yang digunakan
        cap.release()
        cv2.destroyAllWindows()

asyncio.run(main())