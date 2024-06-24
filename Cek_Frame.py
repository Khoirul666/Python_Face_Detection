import cv2

# URL RTSP dari CCTV
rtsp_url = 'rtsp://user:user@192.168.1.37:554/Streaming/Channels/102/'

# Inisialisasi capture video
cap = cv2.VideoCapture(rtsp_url)

# Periksa apakah koneksi berhasil
if not cap.isOpened():
    print("Error: Could not open CCTV stream.")
    exit()

# Baca frame dari stream
ret, frame = cap.read()

# Jika berhasil membaca frame
if ret:
    # Tampilkan frame
    cv2.imshow('CCTV Image', frame)
    cv2.waitKey(0)  # Tunggu sampai tombol apa pun ditekan
    cv2.destroyAllWindows()

# Tutup koneksi
cap.release()
