from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Video, VideoCategory

class VideoForm(forms.ModelForm):
    """Form for video upload and editing."""
    
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter video title')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('Enter video description')}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make video file not required when editing
        if self.instance.pk:
            self.fields['video_file'].required = False
            
        # User-friendly labels
        self.fields['video_file'].label = _('Video File (MP4, AVI, MOV, etc.)')
        self.fields['thumbnail'].label = _('Thumbnail Image')
        
        # Help texts
        self.fields['video_file'].help_text = _('Upload a video file. Maximum size: 1GB.')
        self.fields['thumbnail'].help_text = _('Upload a thumbnail image for your video. If not provided, one will be generated automatically.')
        self.fields['status'].help_text = _('Draft: Only you can see it. Pending Review: Submitted for approval. Published: Visible to everyone.')
        
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file and not self.instance.pk:  # Only validate on new uploads
            # Check file size (limit to 1GB)
            if video_file.size > 1024 * 1024 * 1024:
                raise forms.ValidationError(_('Video file size must be less than 1GB'))
                
            # Check file extension
            allowed_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']
            ext = video_file.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise forms.ValidationError(_('Unsupported file format. Please upload a video in one of the following formats: MP4, AVI, MOV, WMV, FLV, MKV'))
                
        return video_file
        
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            # Check file size (limit to 5MB)
            if thumbnail.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_('Thumbnail image size must be less than 5MB'))
                
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = thumbnail.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise forms.ValidationError(_('Unsupported file format. Please upload an image in one of the following formats: JPG, JPEG, PNG, GIF'))
                
        return thumbnail 