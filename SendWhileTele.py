import asyncio
from telegram import Bot

# Ganti 'YOUR_TOKEN_HERE' dengan token yang kamu dapat dari BotFather
TOKEN = ''
CHAT_ID = ''

async def send_recurring_message(bot):
    while True:
        await bot.send_message(chat_id=CHAT_ID, text='Hello, this is a recurring message')
        await asyncio.sleep(10)  # Tunggu 10 detik sebelum mengirim pesan berikutnya

async def main():
    bot = Bot(token=TOKEN)
    await send_recurring_message(bot)

if __name__ == '__main__':
    asyncio.run(main())