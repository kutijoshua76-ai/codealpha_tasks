import urllib.request
import os

images = {
    'apple_watch.jpg': 'https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg',
    'fujifilm_camera.jpg': 'https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg'
}

media_dir = r"c:\Users\hp\codealpha-E-commerce\media\products\2026\05\05"
os.makedirs(media_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
