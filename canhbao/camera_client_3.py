# from imutils.video import VideoStream, WebcamVideoStream
# import imagezmq
#
#
#
# cap = WebcamVideoStream()
#
# sender = imagezmq.ImageSender(connect_to='tcp://localhost:5566')  # change to IP address and port of server thread
# cam_id = 'Camera 2'  # this name will be displayed on the corresponding camera stream
#
# stream = cap.start()
# i = 0
# while True:
#
#     frame = stream.read()
#     print('Sending ' + str(i))
#     i = i + 1
#     sender.send_image(cam_id, frame)

# read video
from asyncore import loop
import cv2
import imagezmq
import yaml

file = "demo/test2.mp4"
cap = cv2.VideoCapture(file)
sender = imagezmq.ImageSender(connect_to='tcp://localhost:5577')
# change to IP address and port of server thread
cam_id = 'Camera 3'  # this name will be displayed on the corresponding camera stream

#stream = cap.read()
i = 0
while True:
    ret, frame = cap.read()
    if ret:
      # if a frame was returned, send it
      sender.send_image(cam_id, frame)
      i = i+ 1
      print(i)


    else:
      # if no frame was returned, either restart or stop the stream
      if loop:
        cap = cv2.VideoCapture(file)
      else:
        break
