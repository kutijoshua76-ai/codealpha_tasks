import urllib.request
import os

url = "https://images.vestiairecollective.com/cdn-cgi/image/q=80,f=auto,/produit/gucci-gg-marmont-mini-leather-handbag-20516805-1_1.jpg"
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
