import json
import time
from importlib import import_module

import cv2
from django.db import connection
from django.http import HttpResponse, StreamingHttpResponse
from django.http.response import JsonResponse
from django.template import loader
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from canhbao.models.models import Camera, Detection
from django.forms.models import model_to_dict
from django.http import HttpResponseNotFound, JsonResponse
import json


def index(request):
  allcam = Camera.objects.all().values()
  template = loader.get_template('home.html')
  context = {
    'allcam': allcam,
  }
  return HttpResponse(template.render(context, request))


def detailCamera(request, id):
  template = loader.get_template('detail-camera.html')
  print('8329uewijds3ueiwdjsn983weuijdsk83uiewjdsn38uwiejdsn', id)

  camera = Camera.objects.get(id_cam=id)
  # detect = Detection.objects.get(name_cam=camera.name_cam)
  detect_last = Detection.objects.filter(name_cam=camera.name_cam).order_by('-time_detect').values()[1]
  detect = Detection.objects.filter(name_cam=camera.name_cam).order_by('-time_detect').values()[:20:-1]
  cursor = connection.cursor()
  cursor.execute(
    'select distinct y.time_detect1 from (select  DATE_FORMAT(time_detect, "%d-%m-%Y") as  time_detect1, time_detect from canhbao_detection)  as y order by y.time_detect desc limit 10')
  context = {
    'camera': camera,
    'detect': detect,
    'detect_last': detect_last,
    'cursor': cursor
  }
  return HttpResponse(template.render(context, request))


def detailHistory(request, id):
  template = loader.get_template('detail-history.html')
  camera = Camera.objects.get(id_cam=id)
  # detect = Detection.objects.get(name_cam=camera.name_cam)
  detect_last = Detection.objects.filter(name_cam=camera.name_cam).order_by('-time_detect').values()[1]
  detect = Detection.objects.filter(name_cam=camera.name_cam).order_by('-time_detect').values()[:20:-1]
  cursor = connection.cursor()
  cursor.execute(
    'select distinct y.time_detect1 from (select  DATE_FORMAT(time_detect, "%d-%m-%Y") as  time_detect1, time_detect from canhbao_detection)  as y order by y.time_detect desc limit 10')
  context = {
    'camera': camera,
    'detect': detect,
    'detect_last': detect_last,
    'cursor': cursor
  }
  return HttpResponse(template.render(context, request))


def loadDetect(request):
  id = request.GET.get("id", None)
  print('=====================fsdfsdfsdfsfdsdffsdsdfsdffsdsdf#################################', id)
  camera = Camera.objects.get(id_cam=id)
  dct = Detection.objects.filter(name_cam=camera.name_cam).order_by('-time_detect').values()[1]
  # time_dct = dct.get('time_detect')
  # print("ccccccccccccccccccccccccccccc", dct.get('time_detect'))
  return JsonResponse({"dct": dct}, status=200)


def gen(camera_stream, feed_type, device):
  """Video streaming generator function."""
  unique_name = (feed_type, device)

  num_frames = 0
  total_time = 0
  while True:
    time_start = time.time()

    cam_id, frame, prediction = camera_stream.get_frame(unique_name)
    if frame is None:
      break

    num_frames += 1

    time_now = time.time()
    total_time += time_now - time_start
    fps = num_frames / total_time

    # write camera name
    cv2.putText(frame, cam_id, (int(0.75 * frame.shape[1]), int(0.85 * frame.shape[0])), 0, 1.5e-3 * frame.shape[0],
                (0, 255, 255), 2)

    # if feed_type == 'yolo':
    #     cv2.putText(frame, "FPS: %.2f" % fps, (int(0.75 * frame.shape[1]), int(0.9 * frame.shape[0])), 0,
    #                 1.5e-3 * frame.shape[0], (0, 255, 255), 2)

    if prediction == 1:
      print("++++0909999999999904359034295239423904324", prediction)
    frame = cv2.imencode('.jpg', frame)[1].tobytes()  # Remove this line for test camera
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed(request, feed_type, device):
  """Video streaming route. Put this in the src attribute of an img tag."""
  port_list = (5555, 5566)
  if feed_type == 'camera':
    camera_stream = import_module('canhbao.camera_server').Camera
    print(camera_stream)
    print("==========", port_list, " device:", device)
    return StreamingHttpResponse(
      gen(camera_stream=camera_stream(feed_type, device, port_list), feed_type=feed_type, device=device),
      content_type='multipart/x-mixed-replace; boundary=frame')

