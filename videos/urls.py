from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideoListView.as_view(), name='video_list'),
    path('category/<slug:slug>/', views.VideoByCategoryView.as_view(), name='video_by_category'),
    path('upload/', views.VideoUploadView.as_view(), name='video_upload'),
    path('view/<slug:slug>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('edit/<slug:slug>/', views.VideoUpdateView.as_view(), name='video_edit'),
    path('delete/<slug:slug>/', views.VideoDeleteView.as_view(), name='video_delete'),
] 