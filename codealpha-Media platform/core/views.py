from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Profile, Post, Comment, LiveStream
import json

FEED_PAGE_SIZE = 5

def index(request):
    # Initial page load: first batch only. Rest loaded via infinite scroll AJAX.
    sort = request.GET.get('sort', 'trending')
    posts = _sorted_posts(sort)[:FEED_PAGE_SIZE]

    # Suggested users: people the current user isn't following yet
    if request.user.is_authenticated:
        following_ids = request.user.profile.following.all().values_list('user_id', flat=True)
        suggested_profiles = Profile.objects.exclude(user_id=request.user.id).exclude(user_id__in=following_ids)[:5]
    else:
        suggested_profiles = Profile.objects.all()[:5]

    return render(request, 'core/index.html', {
        'posts': posts,
        'suggested_profiles': suggested_profiles,
        'active_sort': sort,
    })


def _sorted_posts(sort):
    """Return a queryset ordered by the requested sort mode."""
    qs = Post.objects.annotate(
        like_count=Count('likes', distinct=True),
        comment_count_ann=Count('comments', distinct=True),
    )
    if sort == 'trending':
        # Trending = likes + comments, recency as tiebreaker
        return qs.order_by('-like_count', '-comment_count_ann', '-created_at')
    # Default: latest first
    return qs.order_by('-created_at')


def feed_api(request):
    """AJAX endpoint: returns JSON list of posts for infinite scroll."""
    sort   = request.GET.get('sort', 'trending')
    page   = int(request.GET.get('page', 1))
    offset = (page - 1) * FEED_PAGE_SIZE

    qs    = _sorted_posts(sort)
    total = qs.count()
    posts = qs[offset: offset + FEED_PAGE_SIZE]

    def post_data(p):
        return {
            'id':          str(p.id),
            'author':      p.author.username,
            'profile_pic': p.author.profile.profile_pic.url if p.author.profile.profile_pic else '',
            'content':     p.content,
            'image':       p.image.url   if p.image  else None,
            'video':       p.video.url   if p.video  else None,
            'like_count':  p.likes.count(),
            'comment_count': p.comments.count(),
            'liked':       request.user in p.likes.all() if request.user.is_authenticated else False,
        }

    return JsonResponse({
        'posts':    [post_data(p) for p in posts],
        'has_more': (offset + FEED_PAGE_SIZE) < total,
        'page':     page,
    })

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj)
    return render(request, 'core/profile.html', {'profile_user': user_obj, 'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        post = Post.objects.create(author=request.user, content=content, image=image, video=video)
        return redirect('index')
    return redirect('index')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text')
        comment = Comment.objects.create(post=post, author=request.user, text=text)
        return JsonResponse({
            'author': comment.author.username,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%b %d, %Y %H:%M')
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_comments(request, post_id):
    """Return all comments for a post as JSON (for the reels comment panel)."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').order_by('created_at')
    data = [
        {
            'author': c.author.username,
            'text': c.text,
            'created_at': c.created_at.strftime('%b %d, %Y %H:%M')
        }
        for c in comments
    ]
    return JsonResponse({'comments': data, 'total': len(data)})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = user_to_follow.profile
    if request.user.profile in profile_to_follow.followers.all():
        profile_to_follow.followers.remove(request.user.profile)
        following = False
    else:
        profile_to_follow.followers.add(request.user.profile)
        following = True
    return JsonResponse({'following': following, 'count': profile_to_follow.followers.count()})

def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return JsonResponse({'success': True})
    return render(request, 'core/signup.html')

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ── Live Streaming ────────────────────────────────────────────────

@login_required
def streams_list(request):
    """Public page showing all active live streams."""
    streams = LiveStream.objects.filter(is_live=True)
    return render(request, 'core/streams.html', {'streams': streams})

@login_required
def go_live(request):
    """Host starts a new live stream."""
    if request.method == 'POST':
        title = request.POST.get('title', f"{request.user.username}'s Stream")
        # End any previous active streams by this user
        LiveStream.objects.filter(host=request.user, is_live=True).update(is_live=False)
        stream = LiveStream.objects.create(host=request.user, title=title)
        return redirect('broadcast', stream_id=stream.id)
    return render(request, 'core/go_live.html')

@login_required
def broadcast(request, stream_id):
    """The broadcaster's page — they share camera/mic via WebRTC."""
    stream = get_object_or_404(LiveStream, id=stream_id, host=request.user)
    return render(request, 'core/broadcast.html', {'stream': stream})

@login_required
def watch_stream(request, stream_id):
    """Viewer's page — they receive the WebRTC stream."""
    stream = get_object_or_404(LiveStream, id=stream_id, is_live=True)
    stream.viewers.add(request.user)
    return render(request, 'core/watch.html', {'stream': stream})

@login_required
def end_stream(request, stream_id):
    """Host ends the stream."""
    stream = get_object_or_404(LiveStream, id=stream_id, host=request.user)
    stream.is_live = False
    stream.save()
    return redirect('streams_list')

def search(request):
    query = request.GET.get('q', '')
    profiles = []
    posts = []
    
    if query:
        # Search users by username or bio
        profiles = Profile.objects.filter(
            Q(user__username__icontains=query) | Q(bio__icontains=query)
        ).distinct()
        
        # Search posts by content
        posts = Post.objects.filter(content__icontains=query).distinct()
        
    return render(request, 'core/search_results.html', {
        'query': query,
        'profiles': profiles,
        'posts': posts,
    })
