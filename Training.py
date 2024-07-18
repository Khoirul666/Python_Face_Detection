from ultralytics import YOLO

# Muat model pralatih YOLOv8
model = YOLO('yolov8n.pt')  # atau model pralatih lainnya

# Latih model menggunakan dataset Anda
model.train(data=r'D:\KHOI\PYTHON\dataset\Full Plat Pengendara.v4i.yolov8\data.yaml', epochs=10, imgsz=640)

# Simpan model yang telah dilatih
model.save('DeteksiPengendara20240718.pt')