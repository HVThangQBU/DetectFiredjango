import sys
import time
from importlib import import_module
import cv2
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from canhbao.models.models import Camera
from django.template.response import TemplateResponse


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
  print("coicam",camera)

  context = {
    'camera': camera,
  }
  return HttpResponse(template.render(context, request))

def gen(camera_stream, feed_type, device):
  """Video streaming generator function."""
  unique_name = (feed_type, device)

  num_frames = 0
  total_time = 0
  while True:
    time_start = time.time()

    cam_id, frame = camera_stream.get_frame(unique_name)
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

    frame = cv2.imencode('.jpg', frame)[1].tobytes()  # Remove this line for test camera
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed(request, feed_type, device):
  import sys
  print(sys.path)
  """Video streaming route. Put this in the src attribute of an img tag."""
  port_list = (5555, 5566)
  if feed_type == 'camera':
    camera_stream = import_module('canhbao.camera_server').Camera
    print(camera_stream)
    print("==========", port_list)
    print(device)
    return StreamingHttpResponse(
      gen(camera_stream=camera_stream(feed_type, device, port_list), feed_type=feed_type, device=device),
      content_type='multipart/x-mixed-replace; boundary=frame')
