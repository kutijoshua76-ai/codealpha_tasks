import os
import django
import requests
import tempfile
from django.core.files import File

# ── Setup Django Environment ──────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibenet.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Post

def add_last_unique():
    url = 'https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4'
    user, _ = User.objects.get_or_create(username='vibe_extra_10')
    print(f"Downloading final unique video: {url}")
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp.write(chunk)
                tmp_path = tmp.name
            
            with open(tmp_path, 'rb') as f:
                post = Post.objects.create(author=user, content='Sample Learning Video. 📚🔊')
                post.video.save('unique_v_10.mp4', File(f), save=True)
            os.remove(tmp_path)
            print("Done!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    add_last_unique()
