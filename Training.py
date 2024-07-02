from ultralytics import YOLO

# Muat model pralatih YOLOv5
model = YOLO('yolov8s.pt')  # atau model pralatih lainnya

# Latih model menggunakan dataset Anda
model.train(data='D:\\KHOI\\PYTHON\\DATASET\\PELANGGAR\\Detection Helm and Number.v3i.yolov8\\data.yaml', epochs=15, imgsz=640)

# Simpan model yang telah dilatih
model.save('Detectionhelm.pt')