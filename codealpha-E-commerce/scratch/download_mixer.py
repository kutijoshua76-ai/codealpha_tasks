import urllib.request
import os

url = "https://www.bhphotovideo.com/images/images2500x2500/kitchenaid_ksm150pser_artisan_series_5_quart_tilt_head_1130006.jpg"
output_path = r"c:\Users\hp\codealpha-E-commerce\media\products\2026\05\05\kitchenaid_mixer.png"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded to {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"Error: {e}")
