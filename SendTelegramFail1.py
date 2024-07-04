import cv2
from ultralytics import YOLO
from io import BytesIO
from telegram import Bot

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def initialize_model(model_path):
    """Initialize YOLO model."""
    return YOLO(model_path)

def process_frame(model, frame):
    """Process frame to perform object detection using YOLO."""
    results = model(frame)
    return results

def draw_boxes_and_labels(frame, results, model):
    """Menggambar kotak pembatas dan label pada frame."""
    for det in results:
        x1, y1, x2, y2 = map(int, det[:4])  # Diasumsikan det berisi [x1, y1, x2, y2, conf, cls]
        conf = det[4]
        cls = int(det[5])
        label = f'{model.names[cls]} {conf:.2f}'
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
    return frame

def crop_and_send_image(frame, box, label, chat_id):
    """Crop the image according to the bounding box and send it to Telegram."""
    x1, y1, x2, y2 = map(int, box[:4])
    cropped_image = frame[y1:y2, x1:x2]
    image_bytes = cv2.imencode('.jpg', cropped_image)[1].tobytes()
    bio = BytesIO(image_bytes)
    bio.name = 'cropped_image.jpg'
    bio.seek(0)
    bot.send_photo(chat_id=chat_id, photo=bio, caption=label)
    print(f'Cropped image sent to Telegram.')

def main(video_source, model_path, chat_id):
    """Main function to run object detection and send results to Telegram."""
    model = initialize_model(model_path)
    cap = cv2.VideoCapture(video_source)

    while True:
        ret, frame = cap.read()

        if not ret or frame is None or frame.size == 0:
            print("Error: Could not read frame from stream or empty frame.")
            break

        results = process_frame(model, frame)
        frame = draw_boxes_and_labels(frame, results, model)

        for result in results.pred:
            for box in result:
                label = f'{model.names[int(box[5])]} {box[4]:.2f}'
                crop_and_send_image(frame, box, label, chat_id)

        cv2.imshow('Original Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_source = 'D:\\KHOI\\PYTHON\\Source\\pengendara motor\\video\\selected\\video100216.jpg'
    model_path = 'D:\\KHOI\\PYTHON\\Coba Python\\Test Detection\\Best.pt'
    main(video_source, model_path, CHAT_ID)
