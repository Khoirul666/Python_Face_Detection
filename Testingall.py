import cv2
import pytesseract
import numpy as np

# Path ke executable Tesseract (sesuaikan dengan path instalasi Anda)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

# Baca gambar
image = cv2.imread(r'D:\KHOI\PYTHON\REF\yolodeteksi\kendara(8).jpg')

# Konversi gambar ke grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Lakukan thresholding
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Gunakan deteksi tepi untuk menyoroti batasan plat
edges = cv2.Canny(binary, 50, 150, apertureSize=3)

# Deteksi kontur
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Variabel untuk menyimpan teks hasil deteksi
detected_text = ""

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = w / float(h)
    if w > 100 and h > 30 and 2 < aspect_ratio < 6:  # Menyesuaikan ukuran dan rasio aspek untuk plat nomor
        # Approximate kontur menjadi sebuah persegi panjang dengan empat titik
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        if len(approx) == 4:
            # Lakukan transformasi perspektif
            pts = approx.reshape(4, 2)
            warped = four_point_transform(image, pts)

            # Tampilkan area yang terdeteksi sebagai plat nomor
            cv2.imshow('Detected Plate', warped)
            cv2.waitKey(0)

            # Ekstraksi teks dari plat yang sudah dipotong dan diluruskan
            text = pytesseract.image_to_string(warped, config='--psm 8')
            detected_text += text
            print("Detected text:", text)

# Tampilkan hasil gambar
cv2.imshow('Original Image', image)
cv2.imshow('Grayscale Image', gray)
cv2.imshow('Binary Image', binary)
cv2.imshow('Edges Image', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
