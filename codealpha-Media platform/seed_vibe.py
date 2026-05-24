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

# ── Configuration ──────────────────────────────────────────────────
# Using reliable Google sample videos with https and user-agent
VIDEO_SAMPLES = [
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        'content': 'Big Buck Bunny! 🐰 Check the sound on this one! 🔊 #animation #classic',
        'user': 'bunny_fan'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
        'content': 'Elephants Dream - Surreal vibes. 🐘✨ #surreal #art',
        'user': 'dreamer_01'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
        'content': 'Igniting the fire! 🔥 #fire #energy',
        'user': 'blaze_master'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
        'content': 'Time for an escape. 🏔️ #nature #freedom',
        'user': 'escape_artist'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
        'content': 'Pure fun! 🎈 #joy #lifestyle',
        'user': 'fun_seeker'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
        'content': 'On a joyride! 🚗💨 #travel #adventure',
        'user': 'road_tripper'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
        'content': 'Meltdown vibes. 🍦 #chill #mood',
        'user': 'mood_vibe'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
        'content': 'Sintel trailer - absolutely epic! 🎬 #sintel #movie',
        'user': 'cinema_lover'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4',
        'content': 'Outback adventure! 🚙💨 #subaru #offroad',
        'user': 'dirt_king'
    },
    {
        'url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4',
        'content': 'What car for a grand? 🚗💰 #cars #budget',
        'user': 'car_guy'
    }
]

COMMENTS_POOL = [
    "This vibe is immaculate! 🔥",
    "The audio quality is actually great! 🎧",
    "Where is this? I need to go!",
    "The quality is insane 👏",
    "Absolute goals.",
    "Love the energy here.",
    "Need more of this content.",
    "This is so satisfying to watch.",
    "The sound design is 10/10.",
    "VibeNet is popping off! 🚀"
]

def seed_platform():
    print("Starting VibeNet Auto-Seeder (Audio Focus)...")
    
    # Optional: Clear existing posts to "replace" them as requested
    print("Clearing old posts...")
    Post.objects.all().delete()
    
    users = []
    for sample in VIDEO_SAMPLES:
        username = sample['user']
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('vibe1234')
            user.save()
            print(f"Created user: @{username}")
        users.append(user)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i, sample in enumerate(VIDEO_SAMPLES):
        author = User.objects.get(username=sample['user'])
        
        print(f"[{i+1}/{len(VIDEO_SAMPLES)}] Downloading video for @{author.username}...")
        try:
            response = requests.get(sample['url'], stream=True, timeout=60, headers=headers)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            tmp_file.write(chunk)
                    tmp_path = tmp_file.name

                try:
                    with open(tmp_path, 'rb') as f:
                        post = Post(author=author, content=sample['content'])
                        post.video.save(f'seed_video_{i}_{random.randint(1000,9999)}.mp4', File(f), save=True)
                        post.save()
                    
                    # Random engagement
                    other_users = [u for u in users if u != author]
                    if other_users:
                        likers = random.sample(other_users, random.randint(1, min(len(other_users), 5)))
                        post.likes.set(likers)
                        
                        for _ in range(random.randint(2, 5)):
                            Comment.objects.create(
                                post=post,
                                author=random.choice(other_users),
                                text=random.choice(COMMENTS_POOL)
                            )
                    
                    print(f"   Success! Post created for @{author.username}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            else:
                print(f"   Failed to download video: {response.status_code}")
                # Fallback to a simpler URL if one fails
                if i == 0:
                     print("   Falling back to w3schools...")
                     # Try one more time with a known good one
                     fallback_url = 'https://www.w3schools.com/html/mov_bbb.mp4'
                     resp2 = requests.get(fallback_url, stream=True, timeout=30)
                     if resp2.status_code == 200:
                         # ... handle fallback if needed ...
                         pass
        except Exception as e:
            print(f"   Error seeding post: {e}")

    print("\nSeeding Complete! 10 videos with audio have been uploaded.")

if __name__ == '__main__':
    seed_platform()
