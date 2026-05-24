import requests
import os

def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30, verify=False)
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
    
    # MDN Washing Machine
    download_image("https://raw.githubusercontent.com/mdn/learning-area/master/javascript/apis/fetching-data/can-store/images/washing-machine.jpg", os.path.join(base_path, "washing_machine.jpg"))
    
    # MDN Iron
    download_image("https://raw.githubusercontent.com/mdn/learning-area/master/javascript/apis/fetching-data/can-store/images/iron.jpg", os.path.join(base_path, "steam_iron.jpg"))
