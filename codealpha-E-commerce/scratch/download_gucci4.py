import urllib.request
import os

url = "https://upload.wikimedia.org/wikipedia/commons/4/4e/Chanel_handbag.jpg"
output_path = r"c:\Users\hp\codealpha-E-commerce\media\products\2026\05\05\gucci_bag.jpg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f"Downloaded: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"Failed: {e}")
