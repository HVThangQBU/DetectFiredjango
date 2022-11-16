from asyncore import loop
import cv2
import imagezmq
import yaml
# with open('config.yml') as f:
#     my_dict = yaml.safe_load(f)
#     print(my_dict)
# file = my_dict["video"]
file = "demo/test.mp4"
cap = cv2.VideoCapture(file)
sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')
# change to IP address and port of server thread
cam_id = 'Camera 1'  # this name will be displayed on the corresponding camera stream

#stream = cap.read()
i = 0
while True:
    ret, frame = cap.read()
    if ret:
      # if a frame was returned, send it
      sender.send_image(cam_id, frame)


    else:
      # if no frame was returned, either restart or stop the stream
      if loop:
        cap = cv2.VideoCapture(file)
      else:
        break
