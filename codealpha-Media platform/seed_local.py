import os
import django
import random
import shutil
from django.core.files import File

# ── Setup Django Environment ──────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibenet.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Post, Profile, Comment

def seed_from_local():
    print("Starting VibeNet Local-Seeder...")
    
    video_dir = os.path.join('media', 'post_videos')
    if not os.path.exists(video_dir):
        print(f"Error: {video_dir} not found.")
        return

    # Filter for the original seed videos (avoiding the ones we just created)
    existing_videos = [f for f in os.listdir(video_dir) if f.startswith('seed_video') and f.endswith('.mp4')]
    if not existing_videos:
        print("Error: No original seed videos found.")
        return

    users_data = [
        ('vibe_master', 'The vibe is immaculate! 🔥 #vibes'),
        ('audio_king', 'Can you hear that? 🔊 #sound #music'),
        ('nature_lover', 'Nature is calling. 🌲✨ #peace'),
        ('dance_queen', 'Wait for the beat drop! 💃🎵 #dance'),
        ('cinema_buff', 'This looks like a movie scene. 🎬 #cinematic'),
        ('adventure_seeker', 'On another level! 🚀 #adventure'),
        ('mood_fix', 'Current mood. 😌 #chill'),
        ('street_vibe', 'City lights and sounds. 🌃 #urban'),
        ('deep_blue', 'Underwater serenity. 🌊 #ocean'),
        ('neon_night', 'Neon vibes only. 💜 #neon'),
    ]

    users = []
    for username, _ in users_data:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('vibe1234')
            user.save()
        users.append(user)

    for i in range(10):
        username, content = users_data[i]
        author = User.objects.get(username=username)
        video_name = random.choice(existing_videos)
        video_path = os.path.join(video_dir, video_name)
        
        try:
            with open(video_path, 'rb') as f:
                post = Post(author=author, content=content)
                post.video.save(f'v_audio_{i}_{random.randint(1000,9999)}.mp4', File(f), save=True)
                post.save()
            print(f"Created post {i}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    seed_from_local()
