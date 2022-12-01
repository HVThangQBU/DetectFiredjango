import canhbao
from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Camera(models.Model):
  id_cam = models.AutoField(primary_key=True)
  name_cam = models.CharField(max_length=100)
  name_location = models.CharField(max_length=100,blank=True)
  location  = models.CharField(max_length=150, blank=True)
  user = models.CharField(max_length=100)




  def __str__(self):
    return self.name_cam


class Detection(models.Model):
  id_detect = models.UUIDField(primary_key=True, default=uuid.uuid4)
  name_detect = name_cam = models.CharField(max_length=100)
  name_cam = models.CharField(max_length=100)
  content = models.TextField()
  image_detect = models.ImageField(upload_to='detect_image', default='bienbao.png')
  time_detect = models.CharField(max_length=100)

  def __str__(self):
    return self.name_detect
