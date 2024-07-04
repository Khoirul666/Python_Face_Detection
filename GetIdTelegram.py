import requests

# Token bot Telegram
TELEGRAM_BOT_TOKEN = '7492865767:AAEFY6PbVOfYprwleADVQW0FL38EHhCYFLQ'

# Endpoint API Telegram
url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'

# Mengirim request ke API Telegram
response = requests.get(url)

# Memeriksa status response
if response.status_code == 200:
    data = response.json()
    print("Response:", data)
    if 'result' in data and len(data['result']) > 0:
        # Mendapatkan chat_id dari pesan terbaru
        chat_id = data['result'][0]['message']['chat']['id']
        print(f'Chat ID: {chat_id}')
    else:
        print("Tidak ada pesan yang diterima oleh bot.")
else:
    print(f"Error {response.status_code}: {response.text}")
