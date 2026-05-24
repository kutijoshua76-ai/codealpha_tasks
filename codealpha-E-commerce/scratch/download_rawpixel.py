import requests
import os

def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.rawpixel.com/',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded {filename} ({len(response.content)} bytes)")
        else:
            print(f"Failed to download {filename}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    base_path = r"media\products\2026\05\05"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    # Accurate Front Load Washing Machine from Rawpixel
    download_image("https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3B4MTIxNTI0OS1pbWFnZS1reWJjZmx1OC5qcGc.jpg", os.path.join(base_path, "washing_machine.jpg"))
    
    # Accurate Professional Steam Iron from Rawpixel
    download_image("https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3B4MTM3NDUwMi1pbWFnZS1reWJjZ3BqZi5qcGc.jpg", os.path.join(base_path, "steam_iron.jpg"))
