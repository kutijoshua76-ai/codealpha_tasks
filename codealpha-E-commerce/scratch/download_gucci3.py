import urllib.request
import os

url = "https://n.nordstrommedia.com/id/sr3/c584ba45-e65b-426b-ae18-f21ef455a163.jpeg"
output_path = r"c:\Users\hp\codealpha-E-commerce\media\products\2026\05\05\gucci_bag.jpg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f"Downloaded: {os.path.getsize(output_path)} bytes")
except Exception as e:
    print(f"Failed: {e}")
