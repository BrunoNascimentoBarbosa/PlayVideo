from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from .models import VideoCategory, Video, VideoView, Course, CourseVideo

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'video_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = _('Videos')

class VideoViewInline(admin.TabularInline):
    model = VideoView
    fields = ('user', 'ip_address', 'viewed_at')
    readonly_fields = ('user', 'ip_address', 'viewed_at')
    extra = 0
    can_delete = False
    max_num = 10
    
    def has_add_permission(self, request, obj=None):
        return False

class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    fields = ('video', 'order')
    extra = 1
    ordering = ('order',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'uploader', 'upload_date', 'view_count', 'get_thumbnail_preview')
    list_filter = ('status', 'category', 'upload_date')
    search_fields = ('title', 'description', 'uploader__email')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('upload_date', 'last_modified', 'publish_date', 'view_count', 'file_size', 'duration', 'video_player', 'get_thumbnail_preview')
    date_hierarchy = 'upload_date'
    actions = ['approve_videos', 'reject_videos']
    inlines = [VideoViewInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'status')
        }),
        (_('Media'), {
            'fields': ('video_file', 'thumbnail', 'video_player', 'get_thumbnail_preview')
        }),
        (_('Upload Info'), {
            'fields': ('uploader', 'reviewer', 'upload_date', 'last_modified', 'publish_date')
        }),
        (_('Technical Details'), {
            'fields': ('view_count', 'duration', 'file_size')
        }),
    )
    
    def video_player(self, obj):
        if obj.video_file:
            return format_html(
                '<video width="320" height="240" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.video_file.url
            )
        return _("No video file")
    
    video_player.short_description = _("Video Preview")
    
    def get_thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        return _("No thumbnail")
    
    get_thumbnail_preview.short_description = _("Thumbnail")
    
    def approve_videos(self, request, queryset):
        updated = queryset.filter(status=Video.PENDING).update(
            status=Video.PUBLISHED,
            reviewer=request.user,
            publish_date=timezone.now()
        )
        self.message_user(request, _(
            f"{updated} video(s) were successfully approved."
        ))
    
    approve_videos.short_description = _("Approve selected videos")
    
    def reject_videos(self, request, queryset):
        updated = queryset.filter(status=Video.PENDING).update(
            status=Video.REJECTED,
            reviewer=request.user
        )
        self.message_user(request, _(
            f"{updated} video(s) were successfully rejected."
        ))
    
    reject_videos.short_description = _("Reject selected videos")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If not admin, only show videos they uploaded or are published
        if not request.user.is_superuser and not request.user.is_editor:
            return qs.filter(uploader=request.user)
        return qs
    
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        # Superusers and editors can change any video
        if request.user.is_superuser or request.user.is_editor:
            return True
        # Users can only change their own videos that aren't published yet
        return obj.uploader == request.user and obj.status != Video.PUBLISHED
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.uploader = request.user
        
        # If status is changing to published, set reviewer and publish date
        if 'status' in form.changed_data and obj.status == Video.PUBLISHED:
            obj.reviewer = request.user
            obj.publish_date = timezone.now()
            
        super().save_model(request, obj, form, change)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'status', 'created_date', 'video_count')
    list_filter = ('status', 'category', 'created_date')
    search_fields = ('title', 'description', 'instructor__email')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_date', 'updated_date', 'get_thumbnail_preview')
    date_hierarchy = 'created_date'
    inlines = [CourseVideoInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'status')
        }),
        (_('Course Info'), {
            'fields': ('instructor', 'thumbnail', 'get_thumbnail_preview')
        }),
        (_('Dates'), {
            'fields': ('created_date', 'updated_date')
        }),
    )
    
    def get_thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" height="auto" />', obj.thumbnail.url)
        return _("No thumbnail")
    
    get_thumbnail_preview.short_description = _("Thumbnail Preview")
    
    def video_count(self, obj):
        return obj.course_videos.count()
    
    video_count.short_description = _('Videos')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If not admin, only show courses they created
        if not request.user.is_superuser and not request.user.is_editor:
            return qs.filter(instructor=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.instructor = request.user
        super().save_model(request, obj, form, change)

@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('course', 'video', 'order')
    list_filter = ('course',)
    search_fields = ('course__title', 'video__title')
    ordering = ('course', 'order')

@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    date_hierarchy = 'viewed_at'
    search_fields = ('video__title', 'user__email', 'ip_address')
    readonly_fields = ('video', 'user', 'ip_address', 'user_agent', 'viewed_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
