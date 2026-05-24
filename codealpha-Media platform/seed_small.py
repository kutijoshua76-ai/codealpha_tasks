import os
import django
import requests
import random
import tempfile
from django.core.files import File

# ── Setup Django Environment ──────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibenet.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Post, Profile, Comment

def seed_small_videos():
    print("Starting VibeNet Small Video Seeder...")
    
    print("Clearing old posts...")
    Post.objects.all().delete()
    
    # Tiny videos for fast loading
    SMALL_VIDEOS = [
        ('https://www.w3schools.com/html/mov_bbb.mp4', 'Tiny Bunny! 🐰'),
        ('https://www.w3schools.com/html/movie.mp4', 'Tiny Bear! 🐻'),
        ('https://vjs.zencdn.net/v/oceans.mp4', 'Tiny Ocean! 🌊'),
    ]

    for i, (url, content) in enumerate(SMALL_VIDEOS):
        user, _ = User.objects.get_or_create(username=f'tester_{i}')
        print(f"Downloading {url}...")
        try:
            response = requests.get(url, stream=True, timeout=20)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
                    for chunk in response.iter_content(chunk_size=4096):
                        tmp.write(chunk)
                    tmp_path = tmp.name
                
                with open(tmp_path, 'rb') as f:
                    post = Post.objects.create(author=user, content=content)
                    post.video.save(f'small_{i}.mp4', File(f), save=True)
                os.remove(tmp_path)
                print(f"Created small post {i}")
        except:
            print(f"Failed to download {url}")

    print("Seeding Complete!")

if __name__ == '__main__':
    seed_small_videos()
