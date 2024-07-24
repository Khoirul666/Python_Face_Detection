import cv2
from ultralytics import YOLO
from io import BytesIO
from telegram import Bot
from telegram.error import TimedOut
import asyncio
import pytesseract

# Token bot Telegram
TELEGRAM_BOT_TOKEN = 'xx'
CHAT_ID = 'xx'

# Inisialisasi bot Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Path video file atau URL stream
no_helm = r'D:\KHOI\PYTHON\dataset\HELM and NO\PICTURE\NO HELM\no_helm 001.jpg'
helm = r'D:\KHOI\PYTHON\dataset\HELM and NO\PICTURE\HELM\helm 001.jpg'
vid_1 = r'D:\KHOI\PYTHON\Source\video\Suasana Jalan Jatingaleh, Semarang saat jam kerja.mp4'
vid_2 = r'D:\KHOI\PYTHON\Source\video\VID20240311151058.mp4'
vid_3 = r'D:\KHOI\PYTHON\Source\video\VID20240316141158.mp4'
vid_4 = r'D:\KHOI\PYTHON\Source\video\WhatsApp Video 2024-07-10 at 12.50.15_07036ddb.mp4'

# Membuka video atau gambar
# cap = cv2.VideoCapture("https://s3.ap-southeast-1.amazonaws.com/moladin.assets/blog/wp-content/uploads/2019/08/15175153/15-Cara-Menjadi-Pengendara-Motor-yang-Baik-di-Jalan-Raya-3.jpg")
cap = cv2.VideoCapture(helm)

# Mengatur ukuran buffer menjadi 3 frame
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

# Tentukan ukuran frame output yang diinginkan
output_width = 1280
output_height = 760
output_width2 = 640
output_height2 = 380

# Model YOLO
# Untuk object pengendara dan memakai helm atau tidak
model2 = YOLO(r"D:\KHOI\PYTHON\runs\detect\train2\weights\best.pt") 
# Untuk mendeteksi plat nomor
model3 = YOLO(r"D:\KHOI\PYTHON\runs\detect\train3\weights\best.pt")

async def kirim_tele(image,label):
    image_convert = cv2.imencode('.jpg',image)[1].tobytes()
    bio = BytesIO(image_convert)
    count = 3
    for attempt in range(count):
        try:
            # await bot.send_photo(chat_id=CHAT_ID,photo=bio,caption=label)
            break
        except TimedOut:
            if attempt<count-1:
                await asyncio.sleep(2)
            else:
                raise

async def plat(plat):
    results = model(plat)
    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])

            # Jika terdeteksi plat maka lakukan pengambilan text dengan OCR
            if(f'{model.names[cls]}'=='plat'):
                crop_image=plat[y1:y2,x1:x2]
                 
                # Jika ingin melihat hasil prosesnya bisa dibuka
                # resized_crop_image = cv2.resize(crop_image, (output_width2, output_height2))
                # cv2.imshow("Plat",resized_crop_image)
                
                skala = 3.0
                c_h = int(crop_image.shape[0] * skala)
                c_w = int(crop_image.shape[1] * skala)
                pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
                ri = cv2.resize(crop_image,(c_w,c_h),interpolation=cv2.INTER_AREA)
                img_gray = cv2.cvtColor(ri,cv2.COLOR_BGR2GRAY)
                th,threshold = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY_INV)
                        
                # Jika ingin melihat hasil prosesnya bisa dibuka
                # resized_threshold = cv2.resize(threshold, (output_width2, output_height2))
                # cv2.imshow('Plat',resized_threshold)
                
                result = ''.join([char for char in result if char.isalnum()])

            if (result!=''):
                return 'Plat nomor gagal dibaca'
            else:
                return 'Palt nomor '+result

async def Pengendara(image):
    # Kirim gambar yang sudah dicrop ke model training
    results = model(image)
    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            
            # Jika didalam gambar yang dicrop terdapat class kepala maka akan diproses kembali
            if(f'{model.names[cls]}'=='kepala'):
                        
                # Jika ingin melihat hasil prosesnya bisa dibuka
                # resized_image = cv2.resize(image, (output_width2, output_height2))
                # cv2.imshow("Kepala",resized_image)
                
                nomor_plat = await plat(image)
                await kirim_tele(image,'pengendara tidak memakai helm, '+nomor_plat)
            # else:
                await kirim_tele(image,'plat tidak terdeteksi oleh sistem')

async def Color(frame,warna,tebal,label,x1,x2,y1,y2):
    cv2.rectangle(frame, (x1, y1), (x2, y2), warna, tebal)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, warna, tebal)

async def main():
    if not cap.isOpened():
        print("Error: Tidak dapat membuka video atau gambar.")
    else:
        while True:
            ret,frame = cap.read()

            if not ret:
                print("Error: Tidak dapat membaca frame dari stream.")
                break

            if frame is None or frame.size == 0:
                print("Error: Frame kosong.")
                continue
            
            # Kirim file ke model training
            results = model3(frame)
            # results_resized = model2(frame)
            # results3 = model3(frame)

            # Mendapatkan hasil deteksi
            for result in results:
            #     print(result)
                for box in result.boxes:
            #         print(box)
                    x1,y1,x2,y2 = map(int,box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    cv2.putText(frame, f'{model3.names[cls]} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 1)
                    # print(f'{model.names[cls]}')
                    # if(f'{model.names[cls]}'=='Plat Nomor'):
                        # print('Playbascaslcac')
                #     # Crop gambar jika terdeteksi pengendara
                    # if(f'{model.names[cls]}'=='pengendara'):
                    #     crop_image=frame[y1:y2,x1:x2]

                #         # await Pengendara(crop_image)
                        
                #         # Jika ingin melihat hasil prosesnya bisa dibuka
                #         skala = crop_image.shape[1] / output_width2
                #         print(skala)
                #         print(crop_image.shape)
                #         lebar = int(crop_image.shape[1] / skala)
                #         tinggi = int(crop_image.shape[0] / skala)
                #         resized_crop_image = cv2.resize(crop_image, (lebar, tinggi))
                #         cv2.imshow("Crop",resized_crop_image)
                    
                #         # if cv2.waitKey(1) & 0xFF == ord('q'):
                #         #     break


                    # # Gambar class helm dengan kotak hijau dan beri warna hijau dan tebal 1px serta label
                    # if(f'{model.names[cls]}'=='Memakai Helm'):
                    #     await Color(frame,(0, 255, 0),1,f'{model.names[cls]} {conf:.2f}',x1,x2,y1,y2)

                    # # Gambar class kepala dengan kotak merah dan beri warna merah dan tebal 1px serta label
                    # if(f'{model.names[cls]}'=='Tidak Memakai Helm'):
                    #     await Color(frame,(255, 0, 255),1,f'{model.names[cls]} {conf:.2f}',x1,x2,y1,y2)

                    # # Gambar class pengendara dengan kotak biru dan beri warna biru dan tebal 1px serta label
                    # if(f'{model.names[cls]}'=='Pengendara'):
                    #     await Color(frame,(255, 0, 0),1,f'{model.names[cls]} {conf:.2f}',x1,x2,y1,y2)

                    # # Gambar class plat dengan kotak magenta dan beri warna magenta dan tebal 1px serta label
                    # if(f'{model.names[cls]}'=='Plat Nomor'):
                    #     print('plat')
                    #     await Color(frame,(255, 0, 255),1,f'{model.names[cls]} {conf:.2f}',x1,x2,y1,y2)


            # Ubah ukuran frame
            resized_frame = cv2.resize(frame, (output_width, output_height))

            # Tampilkan video atau gambar yang sudah diproses
            cv2.imshow('Output', frame)
            # cv2.imshow('Output2', resized_frame)
            # cv2.imshow('Output3', results3)

            # Menunggu dan Jika ditekan tombol 'q' maka akan menutup
            if cv2.waitKey(50000) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

asyncio.run(main())