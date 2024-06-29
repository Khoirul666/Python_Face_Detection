import cv2

# Path video file atau URL stream
video_source = 'rtsp://admin:admin@192.168.1.37:8554/Streaming/Channels/101'

# Membuka video
cap = cv2.VideoCapture(video_source)

# Tentukan ukuran frame output yang diinginkan
output_width = 640
output_height = 480

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

        # Ubah ukuran frame
        resized_frame = cv2.resize(frame, (output_width, output_height))

        # Tampilkan frame yang diubah ukurannya
        cv2.imshow('Kamera CCTV', resized_frame)

        # Tekan 'q' untuk keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release semua resource yang digunakan
    cap.release()
    cv2.destroyAllWindows()
