from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

class VideoCategory(models.Model):
    """Category for organizing videos."""
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('video category')
        verbose_name_plural = _('video categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Course(models.Model):
    """Course model for organizing a collection of videos."""
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    thumbnail = models.ImageField(_('thumbnail'), upload_to='course_thumbnails/', blank=True, null=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    category = models.ForeignKey(
        VideoCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='courses'
    )
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_date = models.DateTimeField(_('updated date'), auto_now=True)
    
    # Status choices like Video
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
        (ARCHIVED, _('Archived')),
    ]
    
    status = models.CharField(
        _('status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=DRAFT
    )
    
    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('videos:course_detail', kwargs={'slug': self.slug})
    
    @property
    def video_count(self):
        return CourseVideo.objects.filter(course=self).count()

class Video(models.Model):
    """Video model with storage on S3."""
    
    # Status choices
    DRAFT = 'draft'
    PENDING = 'pending'
    PUBLISHED = 'published'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (DRAFT, _('Draft')),
        (PENDING, _('Pending Review')),
        (PUBLISHED, _('Published')),
        (REJECTED, _('Rejected')),
    ]
    
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    video_file = models.FileField(_('video file'), upload_to='videos/')
    thumbnail = models.ImageField(_('thumbnail'), upload_to='thumbnails/', blank=True, null=True)
    category = models.ForeignKey(
        VideoCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='videos'
    )
    status = models.CharField(
        _('status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=DRAFT
    )
    
    # Meta data
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_videos'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_videos'
    )
    upload_date = models.DateTimeField(_('upload date'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    publish_date = models.DateTimeField(_('publish date'), null=True, blank=True)
    
    # Stats
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    
    # Technical details
    duration = models.PositiveIntegerField(_('duration in seconds'), null=True, blank=True)
    file_size = models.PositiveIntegerField(_('file size in bytes'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('videos:video_detail', kwargs={'slug': self.slug})
    
    def get_courses(self):
        """Return all courses this video belongs to"""
        return Course.objects.filter(coursevideo__video=self)

class CourseVideo(models.Model):
    """Association model between Course and Video with ordering."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_courses')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _('course video')
        verbose_name_plural = _('course videos')
        ordering = ['course', 'order']
        unique_together = ['course', 'video']  # Each video can only appear once in a course
    
    def __str__(self):
        return f"{self.course.title} - {self.video.title}"
    
    def next_video(self):
        """Get the next video in the course sequence"""
        next_videos = CourseVideo.objects.filter(
            course=self.course, 
            order__gt=self.order
        ).order_by('order')
        
        return next_videos.first().video if next_videos.exists() else None
    
    def previous_video(self):
        """Get the previous video in the course sequence"""
        prev_videos = CourseVideo.objects.filter(
            course=self.course, 
            order__lt=self.order
        ).order_by('-order')
        
        return prev_videos.first().video if prev_videos.exists() else None

class VideoView(models.Model):
    """Track video views."""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='video_views'
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('video view')
        verbose_name_plural = _('video views')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.video.title} - {self.viewed_at}"
