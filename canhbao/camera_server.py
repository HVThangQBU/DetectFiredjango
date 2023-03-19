
import cv2
import time
from canhbao import detectionfire
from canhbao.detectionfire import CameraDetectionFire
from canhbao.base_camera import BaseCamera
import datetime
import os

from canhbao.models.models import Detection


class Camera(BaseCamera):

    def __init__(self, feed_type, device, port_list):
      super(Camera, self).__init__(feed_type, device, port_list)
    

    @staticmethod
    def server_frames(image_hub):
        num_frames = 0
        total_time = 0
        end =0
        while True:  # main loop
            time_start = time.time()

            cam_id, frame = image_hub.recv_image()

            image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern

            print("camera ID", cam_id)
            num_frames += 1
            # detection fire
            # Test = CameraDetectionFire()
          
            prediction,frame = detectionfire.CameraDetectionFire().dectection_fire(frame)
            print("==========================================prediction: ",prediction)
            localtime = datetime.datetime.now()
            height, width, _ = frame.shape
            if prediction == 1:
              print("cul", prediction)
              print(f'\t\t|____No-Fire')
              # cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 10)
              cv2.putText(frame, 'No-Fire', (int(width / 16), int(height / 4)),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 00), 2, cv2.LINE_AA)
            else:
              print("cul", prediction)
              print(f'\t\t|____Fire')
              try:
                os.mkdir("media/detect_image/" + cam_id)
              except:
                print("An exception occurred")
              try:
                datestring = localtime.strftime("%Y-%m-%d")
                now = datetime.datetime.now().second
              
                print(datestring, "=======================================================================", cam_id)

                os.mkdir("media/detect_image/" + cam_id + "/" + datestring)
              except:
                print("An exception occurred")
              today = datetime.datetime.now()
              print(today.strftime("%Y-%m-%d"))
            
              # if int(localtime.second) % 2 == 0:
              if (now != end) & (int(now - end) % 2 == 0):
                print("=======================================END END END",end)
               # print(str(threading.current_thread().ident) + " Phat hien chay " + str(today))
                cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 30)
                out_path = "media/detect_image/" + cam_id + "/" + datestring
                datefull = localtime.strftime("%Y-%m-%d %H:%M:%S")
                # localtime.strftime("%d %H-%M-%S")
                frame_name = localtime.strftime("%d %H-%M-%S") + '.jpg'
                cv2.imwrite(os.path.join(out_path, frame_name), frame)
                name = "Phat hien chay"
                content = " co dam chay"
              
               
                end = datetime.datetime.now().second
                dec = Detection.objects.create(name_detect=name, name_cam=cam_id, content=content,
                                               image_detect="detect_image/" + cam_id + "/" + datestring + "/" + frame_name,
                                               time_detect=datefull)
                dec.save()

              cv2.putText(frame, 'Fire', (int(width / 16), int(height / 4)),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            time_now = time.time()
            total_time += time_now - time_start
            fps = num_frames / total_time
                      # uncomment below to see FPS of camera stream
            cv2.putText(frame, "FPS: %.2f" % fps, (int(20), int(40 * 5e-3 * frame.shape[0])), 0, 2e-3 * frame.shape[0],(255, 255, 255), 2)


            yield cam_id, frame, prediction
