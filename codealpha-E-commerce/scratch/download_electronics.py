import urllib.request
import os

images = {
    'sony_headphones.jpg': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    'iphone_pro.jpg': 'https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=800&q=80',
    'apple_watch.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80',
    'fujifilm_camera.jpg': 'https://images.unsplash.com/photo-1504274066651-8d31a536b11a?w=800&q=80'
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
