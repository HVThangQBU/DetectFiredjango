from django.contrib import admin
from canhbao.models.models import Camera,Detection, CustomUser
# #
admin.site.register(Camera)
# #
admin.site.register(Detection)
# Register your models here.
admin.site.register(CustomUser)