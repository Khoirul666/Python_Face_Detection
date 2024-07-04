import asyncio
from telegram import Bot

# Ganti 'YOUR_TOKEN_HERE' dengan token yang kamu dapat dari BotFather
TOKEN = '7492865767:AAEFY6PbVOfYprwleADVQW0FL38EHhCYFLQ'
CHAT_ID = '2135671506'
IMAGE_PATH = 'D:\\KHOI\\PYTHON\\Source\\pengendara motor\\video\\selected\\video100186.jpg'  # Ganti dengan path ke gambar yang ingin kamu kirim

async def send_recurring_image(bot):
    while True:
        with open(IMAGE_PATH, 'rb') as image:
            await bot.send_photo(chat_id=CHAT_ID, photo=image)
        # await asyncio.sleep(10)  # Tunggu 10 detik sebelum mengirim pesan berikutnya

async def main():
    bot = Bot(token=TOKEN)
    await send_recurring_image(bot)

if __name__ == '__main__':
    asyncio.run(main())
