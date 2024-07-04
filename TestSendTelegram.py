import requests

# Token bot Telegram
TELEGRAM_BOT_TOKEN = '7492865767:AAEFY6PbVOfYprwleADVQW0FL38EHhCYFLQ'
CHAT_ID = '2135671506'

# Pesan yang ingin dikirim
MESSAGE = 'Test Pesan'

# Endpoint API Telegram untuk mengirim pesan
url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# Data yang akan dikirimkan ke endpoint API
payload = {
    'chat_id': CHAT_ID,
    'text': MESSAGE
}

# Mengirim request POST ke API Telegram
response = requests.post(url, data=payload)

# Memeriksa status response
if response.status_code == 200:
    print("Pesan berhasil dikirim")
else:
    print(f"Error {response.status_code}: {response.text}")
