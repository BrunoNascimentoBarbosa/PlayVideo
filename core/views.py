from django.shortcuts import render
from django.views.generic import TemplateView
from videos.models import Video, VideoCategory

# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar vídeos em destaque ou recentes se necessário
        context['featured_videos'] = Video.objects.filter(status=Video.PUBLISHED).order_by('-publish_date')[:6]
        context['categories'] = VideoCategory.objects.all()[:8]
        return context
