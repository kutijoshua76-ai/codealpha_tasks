import urllib.request
import os

url = "https://media.gucci.com/style/DarkGray_Center_0_0_800x800/1585848606/446744_DTDIT_1000_001_100_0000_Light-GG-Marmont-mini-shoulder-bag.jpg"
output_path = r"c:\Users\hp\codealpha-E-commerce\media\products\2026\05\05\gucci_bag.jpg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f"Downloaded successfully: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"Failed: {e}")
