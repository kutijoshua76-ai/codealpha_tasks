from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feed/', views.feed_api, name='feed_api'),
    path('search/', views.search, name='search'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<uuid:post_id>/like/', views.like_post, name='like_post'),
    path('post/<uuid:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<uuid:post_id>/comments/', views.get_comments, name='get_comments'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Live Streaming
    path('live/', views.streams_list, name='streams_list'),
    path('live/go/', views.go_live, name='go_live'),
    path('live/broadcast/<uuid:stream_id>/', views.broadcast, name='broadcast'),
    path('live/watch/<uuid:stream_id>/', views.watch_stream, name='watch_stream'),
    path('live/end/<uuid:stream_id>/', views.end_stream, name='end_stream'),
]
