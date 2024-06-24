import requests

def is_ip_camera(ip):
    try:
        response = requests.get(f"http://{ip}", timeout=5)
        if response.status_code == 200:
            if "camera" in response.text.lower() or "stream" in response.text.lower():
                return True
    except requests.RequestException:
        pass
    return False

ip_address = "192.168.1.37"  # Ganti dengan IP yang ingin diuji

if is_ip_camera(ip_address):
    print(f"{ip_address} adalah IP kamera.")
else:
    print(f"{ip_address} bukan IP kamera.")
