import pytesseract
from ultralytics import YOLO
import cv2

file = r'D:\KHOI\PYTHON\REF\yolodeteksi\kendara(8).jpg'

cap = cv2.VideoCapture(file)

model = YOLO(r"D:\KHOI\PYTHON\epochs=200_imgsz640.pt")

# Fungsi untuk melakukan transformasi perspektif
def four_point_transform(image, pts):
    rect = np.array(pts, dtype="float32")
    (tl, tr, br, bl) = rect

    # Lebar plat baru adalah jarak antara titik kanan atas dan kiri atas atau kanan bawah dan kiri bawah
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    # Tinggi plat baru adalah jarak antara titik kanan atas dan kanan bawah atau kiri atas dan kiri bawah
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    # Koordinat tujuan dari plat yang diluruskan
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # Matrik transformasi perspektif
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

while True:
    ret,frame = cap.read()

    if not ret:
        print("Error: Tidak dapat membaca frame dari stream.")
        break

    if frame is None or frame.size == 0:
        print("Error: Frame kosong.")
        continue

    results = model(frame)
    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])

            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            # cv2.putText(frame, f'{model.names[cls]} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 1)

            if(f'{model.names[cls]}'=='Plat Nomor' and conf > 0.5 ):
                crop_image = frame[y1:y2,x1:x2]
                # cv2.imshow('Crop',crop_image)
                
                # Cek ukuran frame
                height, width, channels = crop_image.shape
                # print(f"Ukuran frame: {width}x{height}")

                if width<640:
                    skala=640/width
                    resize = cv2.resize(crop_image, (int(width*skala), int(height*skala)))
                    cv2.imshow('resized',resize)

                    # Konversi gambar ke grayscale
                    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
                    img_gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('bgcolor', img_gray)

                    # Lakukan thresholding
                    _,threshold = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY_INV)
                    cv2.imshow('Threshold',threshold)
                    
                    # Gunakan deteksi tepi (optional, tergantung pada kualitas gambar)
                    edges = cv2.Canny(threshold, 50, 150, apertureSize=3)
                    cv2.imshow('Edge',edges)

                

                    ocr_result = pytesseract.image_to_string(edges,config='--psm 8')
                    ocr_result = ocr_result.upper()

                    tulisan = ''.join([char for char in ocr_result if char.isalnum()])
                    # print(tulisan)
                    if tulisan!='':
                        print(tulisan)
                    else:
                        print('kosong')

    cv2.imshow('Output',frame)

    if cv2.waitKey(50000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()