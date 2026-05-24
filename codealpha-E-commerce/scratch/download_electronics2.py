import urllib.request
import os

images = {
    'apple_watch.jpg': 'https://upload.wikimedia.org/wikipedia/commons/a/ae/Apple_Watch_Series_5.jpg',
    'fujifilm_camera.jpg': 'https://upload.wikimedia.org/wikipedia/commons/b/b3/Fujifilm_X-T1.jpg'
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
