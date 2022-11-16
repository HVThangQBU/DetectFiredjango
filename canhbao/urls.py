
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index),
  path('video_feed/<feed_type>/<device>/', views.video_feed, name='video_feed'),
  path('detail_camera/', views.detailCamera, name='detail_camera')
]
