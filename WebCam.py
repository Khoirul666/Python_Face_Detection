import cv2

cap = cv2.VideoCapture(0)

while True:
    # Baca frame-by-frame
    ret, frame = cap.read()
    
    # Tampilkan frame
    cv2.imshow('Webcam Feed', frame)
    
    # Tunggu tombol key 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Setelah loop selesai, lepaskan capture dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
