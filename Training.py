from ultralytics import YOLO

# Muat model pralatih YOLOv8
model = YOLO('yolov8n.pt')  # atau model pralatih lainnya

# Konfigurasi pelatihan
train_cfg = {
    'data': r'D:\KHOI\PYTHON\dataset\Detection Plat.v3i.yolov8\data.yaml',  # Ganti dengan path ke file data.yaml Anda
    'epochs': 500,  # Set jumlah epoch menjadi 500
    'imgsz': 640,  # Ukuran gambar (ubah sesuai kebutuhan)
    'batch': 16,  # Ukuran batch (ubah sesuai kebutuhan)
    'patience': 0,  # Set nilai patience untuk EarlyStopping
    'device': 'cpu',  # Ubah sesuai perangkat Anda ('0' untuk GPU, 'cpu' untuk CPU)
}

# Mulai pelatihan
model.train(**train_cfg)

# Simpan model yang telah dilatih
model.save('DeteksiPengendara20240805.pt')