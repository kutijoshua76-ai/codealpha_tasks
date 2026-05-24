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

def seed_guaranteed_sound():
    print("Starting VibeNet Seeder (Guaranteed Sound)...")
    
    print("Clearing old posts...")
    Post.objects.all().delete()
    
    # These files are explicitly labeled as "with audio"
    SOUND_VIDEOS = [
        ('https://filesamples.com/samples/video/mp4/sample_960x400_ocean_with_audio.mp4', 'Ocean waves with soothing sound. 🌊🔊'),
        ('https://filesamples.com/samples/video/mp4/sample_1280x720_surfing_with_audio.mp4', 'Surfing vibes! 🏄‍♂️🎵'),
        ('https://filesamples.com/samples/video/mp4/sample_640x360.mp4', 'City life and sound. 🌆🎧'),
        ('https://www.w3schools.com/html/mov_bbb.mp4', 'Big Buck Bunny (Classic Sound). 🐰🔊'),
        ('https://vjs.zencdn.net/v/oceans.mp4', 'Deep Sea Audio. 🌊🐋'),
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i in range(10):
        url, base_content = random.choice(SOUND_VIDEOS)
        content = f"{base_content} - Post #{i+1}"
        user, _ = User.objects.get_or_create(username=f'vibe_user_{i}')
        
        print(f"[{i+1}/10] Downloading {url}...")
        try:
            response = requests.get(url, stream=True, timeout=30, headers=headers)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
                    for chunk in response.iter_content(chunk_size=8192):
                        tmp.write(chunk)
                    tmp_path = tmp.name
                
                with open(tmp_path, 'rb') as f:
                    post = Post.objects.create(author=user, content=content)
                    post.video.save(f'sound_v_{i}_{random.randint(1000,9999)}.mp4', File(f), save=True)
                    print(f"   Created post {i}")
                os.remove(tmp_path)
            else:
                print(f"   Failed: {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")

    print("Seeding Complete!")

if __name__ == '__main__':
    seed_guaranteed_sound()
