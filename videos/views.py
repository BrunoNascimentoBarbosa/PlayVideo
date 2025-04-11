from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.db import models
from .models import Video, VideoCategory, VideoView
from .forms import VideoForm

class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Video.objects.filter(status=Video.PUBLISHED)
        
        # Filter by category if specified
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Filter by search query if specified
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) | 
                models.Q(description__icontains=search_query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = VideoCategory.objects.all()
        # Pass search query to template for form
        context['search_query'] = self.request.GET.get('search', '')
        return context

class VideoByCategoryView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(VideoCategory, slug=self.kwargs['slug'])
        return Video.objects.filter(category=self.category, status=Video.PUBLISHED)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = VideoCategory.objects.all()
        context['current_category'] = self.category
        return context

class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'
    
    def get_queryset(self):
        # Regular users can only see published videos
        if self.request.user.is_staff or self.request.user.is_editor:
            return Video.objects.all()
        elif self.request.user.is_authenticated:
            # Regular users can see published videos and their own videos
            return Video.objects.filter(
                models.Q(status=Video.PUBLISHED) | 
                models.Q(uploader=self.request.user)
            )
        else:
            # Anonymous users can only see published videos
            return Video.objects.filter(status=Video.PUBLISHED)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_videos'] = Video.objects.filter(
            status=Video.PUBLISHED,
            category=self.object.category
        ).exclude(id=self.object.id)[:6]
        
        # Debug info para diagnóstico de problemas de reprodução
        video = self.object
        context['debug_info'] = {
            'file_url': video.video_file.url if video.video_file else None,
            'file_name': video.video_file.name if video.video_file else None,
            'file_size': video.file_size,
            'content_type': getattr(video.video_file, 'content_type', 'unknown') if video.video_file else None,
        }
        
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        # Record view if not the uploader
        if request.user != self.object.uploader:
            # Get client IP and user agent
            ip = self.request.META.get('REMOTE_ADDR', None)
            user_agent = self.request.META.get('HTTP_USER_AGENT', '')
            
            # Create video view
            VideoView.objects.create(
                video=self.object,
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip,
                user_agent=user_agent
            )
            
            # Update view count
            self.object.view_count += 1
            self.object.save(update_fields=['view_count'])
            
        return response

class VideoUploadView(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_upload.html'
    success_url = reverse_lazy('videos:video_list')
    
    def form_valid(self, form):
        form.instance.uploader = self.request.user
        # If user is admin or editor, allow direct publishing
        if self.request.user.is_editor or self.request.user.is_admin:
            if form.instance.status == Video.PUBLISHED:
                form.instance.publish_date = timezone.now()
                form.instance.reviewer = self.request.user
        else:
            # Regular users can only submit for review or save as draft
            if form.instance.status == Video.PUBLISHED:
                form.instance.status = Video.PENDING
                
        # Get file size if available
        if form.instance.video_file:
            form.instance.file_size = form.instance.video_file.size
            
        return super().form_valid(form)

class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_update.html'
    
    def test_func(self):
        video = self.get_object()
        # Check if user is the uploader or has editor/admin permissions
        return (self.request.user == video.uploader or 
                self.request.user.is_editor or 
                self.request.user.is_admin)
    
    def get_success_url(self):
        return reverse_lazy('videos:video_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        # If regular user is updating a published video, change status to pending
        if not (self.request.user.is_editor or self.request.user.is_admin):
            if self.object.status == Video.PUBLISHED and form.has_changed():
                form.instance.status = Video.PENDING
                
        # If admin/editor is setting to published
        if (self.request.user.is_editor or self.request.user.is_admin) and form.instance.status == Video.PUBLISHED:
            if self.object.status != Video.PUBLISHED:
                form.instance.publish_date = timezone.now()
                form.instance.reviewer = self.request.user
                
        return super().form_valid(form)

class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videos/video_confirm_delete.html'
    success_url = reverse_lazy('videos:video_list')
    
    def test_func(self):
        video = self.get_object()
        # Check if user is the uploader or has admin permissions
        return self.request.user == video.uploader or self.request.user.is_admin
