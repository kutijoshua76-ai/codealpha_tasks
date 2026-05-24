from django.contrib import admin
from .models import Profile, Post, Comment, LiveStream


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'text', 'created_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower_count', 'following_count')
    search_fields = ('user__username', 'bio')

    @admin.display(description='Followers')
    def follower_count(self, obj):
        return obj.followers.count()

    @admin.display(description='Following')
    def following_count(self, obj):
        return obj.following.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'short_content', 'has_image', 'has_video', 'like_count', 'comment_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')
    readonly_fields = ('id', 'created_at', 'likes')
    inlines = [CommentInline]

    @admin.display(description='Content')
    def short_content(self, obj):
        return (obj.content[:60] + '…') if len(obj.content) > 60 else obj.content or '(media only)'

    @admin.display(description='Image', boolean=True)
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(description='Video', boolean=True)
    def has_video(self, obj):
        return bool(obj.video)

    @admin.display(description='Likes')
    def like_count(self, obj):
        return obj.likes.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'short_text', 'created_at')
    search_fields = ('author__username', 'text')
    list_filter = ('created_at',)

    @admin.display(description='Comment')
    def short_text(self, obj):
        return (obj.text[:80] + '…') if len(obj.text) > 80 else obj.text


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('host', 'title', 'is_live', 'viewer_count', 'started_at')
    list_filter = ('is_live',)
    search_fields = ('host__username', 'title')
    readonly_fields = ('id', 'started_at')
    actions = ['end_selected_streams']

    @admin.display(description='Viewers')
    def viewer_count(self, obj):
        return obj.viewers.count()

    @admin.action(description='End selected streams')
    def end_selected_streams(self, request, queryset):
        updated = queryset.update(is_live=False)
        self.message_user(request, f'{updated} stream(s) ended.')
