import cv2
import requests
from bs4 import BeautifulSoup

# Sharelink yang mengarah ke halaman web
sharelink = 'https://m-us.smart321.com/AZ8zKB12IfpY5x6y'

# Mendapatkan konten halaman web
response = requests.get(sharelink)
soup = BeautifulSoup(response.text, 'html.parser')

# Mengurai URL stream video dari halaman web
# (sesuaikan ini dengan struktur halaman web Anda)
video_tag = soup.find('video')
stream_url = video_tag['src']

# Membuka stream video
cap = cv2.VideoCapture(stream_url)

# Mengecek apakah stream berhasil dibuka
if not cap.isOpened():
    print("Error: Tidak dapat membuka video stream")
else:
    while True:
        # Membaca frame dari stream
        ret, frame = cap.read()
        
        # Jika frame berhasil dibaca
        if ret:
            # Menampilkan frame
            cv2.imshow('IP Camera Stream', frame)
            
            # Tekan 'q' untuk keluar dari loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Tidak dapat membaca frame dari stream")
            break

# Membersihkan resource
cap.release()
cv2.destroyAllWindows()
