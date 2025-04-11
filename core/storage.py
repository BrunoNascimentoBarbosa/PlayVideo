from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import os

class MediaStorage(S3Boto3Storage):
    """
    Custom S3 storage class for media files (user uploads).
    """
    location = 'media'
    file_overwrite = False
    
class StaticStorage(S3Boto3Storage):
    """
    Custom S3 storage class for static files.
    """
    location = 'static'

class VideoStorage(S3Boto3Storage):
    """
    Custom S3 storage class for video files with specific configurations.
    """
    location = 'videos'
    file_overwrite = False
    
    def get_available_name(self, name, max_length=None):
        """
        Generate a unique file name for the video by appending a timestamp.
        """
        name, ext = os.path.splitext(name)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{name}_{timestamp}{ext}" 