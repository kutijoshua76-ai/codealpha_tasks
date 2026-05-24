import urllib.request
import os

images = {
    'nike_sneakers.jpg': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
    'gucci_bag.jpg': 'https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=800&q=80',
    'biker_jacket.jpg': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80',
    'prada_sunglasses.jpg': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80'
}

media_dir = r"c:\Users\hp\codealpha-E-commerce\media\products\2026\05\05"
os.makedirs(media_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for filename, url in images.items():
    output_path = os.path.join(media_dir, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded {filename}: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Failed {filename}: {e}")
