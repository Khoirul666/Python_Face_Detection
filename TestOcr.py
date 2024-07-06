import pytesseract
from PIL import Image
import cv2

async def main():
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Lenovo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Adjust this path according to your installation
        img_path = r'D:\KHOI\PYTHON\Source\pengendara motor\Dataset Plat Nomor\kode-angka-plat-nomor.png'
        
        # Open the image using PIL (Python Imaging Library)
        img = Image.open(img_path)

        # Perform OCR with pytesseract
        text = pytesseract.image_to_string(img)
        
        print("OCR Result:")
        print(text)

        image = cv2.VideoCapture(img_path)
        cv2.imshow(image)

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
