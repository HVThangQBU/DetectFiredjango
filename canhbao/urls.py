
from . import views
from django.urls import path

urlpatterns = [
  path('home', views.index, name='home'),
  path('video_feed/<feed_type>/<device>/', views.video_feed, name='video_feed'),
  path('detail_camera/<int:id>', views.detailCamera, name='detail_camera'),
  path('load_detect', views.loadDetect, name = "load_detect"),
  path('detail_camera/detail_history/<int:id>', views.detailHistory, name='detail_history')
]

