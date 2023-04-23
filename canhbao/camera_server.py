import cv2
import time
from canhbao import detectionfire
from canhbao.detectionfire import CameraDetectionFire
from canhbao.base_camera import BaseCamera
import datetime
import os
from django.utils import timezone
from canhbao.models.models import Detection
from canhbao.models.models import Camera as myCam

class Camera(BaseCamera):
   
    def __init__(self, feed_type, device, port_list):
    
        super(Camera, self).__init__(feed_type, device, port_list)

    @staticmethod
    def server_frames(image_hub):
        num_frames = 0
        total_time = 0
        end = 0


        detector = CameraDetectionFire()
        while True:  # main loop
            time_start = time.time()

            cam_id, frame = image_hub.recv_image()
            image_hub.send_reply(
                b"OK"
            )  # this is needed for the stream to work with REQ/REP pattern

            print("camera ID", cam_id)
            num_frames += 1

        # from collections import defaultdict

        # # Create a dictionary to store the last received frame for each camera
        # last_frames = defaultdict(lambda: None)
        # print("co last_frame", last_frames)

        # # Define a timeout value (in seconds)
        # timeout = 1

        # while True:
        #     time_start = time.time()

        #     cam_id, frame = image_hub.recv_image()

        #     image_hub.send_reply(
        #         b"OK"
        #     )  # this is needed for the stream to work with REQ/REP pattern

        #     print("camera ID", cam_id)
        #     num_frames += 1

        #     # Check if the current camera has sent a frame before
        #     if last_frames[cam_id] is not None:
        #         # Calculate the time elapsed since the last frame was received
        #         elapsed_time = time_start - last_frames[cam_id]
                
        #         # Check if the elapsed time exceeds the timeout value
        #         if elapsed_time > timeout:
        #             # Close the connection to the camera
        #             image_hub.disconnect(cam_id)
        #             last_frames[cam_id] = None
        #             print(f"Connection to {cam_id} closed due to timeout")
            
        #     # Store the timestamp of the current frame for the current camera
        #     last_frames[cam_id] = time_start
    
   

            # detection fire
            # Test = CameraDetectionFire()
            
     
            prediction, frame = detector.detection_fire(frame)
            # print("==========================================prediction: ",prediction)
            localtime = datetime.datetime.now()
            height, width, _ = frame.shape
            now = datetime.datetime.now()
            # Định dạng chuỗi ngày giờ
            formatted_date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            cv2.putText(
                frame,
                "Time: " + str(formatted_date_time),
                (int(20), int(15 * 5e-3 * frame.shape[0])),
                0,
                2e-3 * frame.shape[0],
                (255, 255, 255),
                2,
            )
            if prediction == 1:
                # print("cul", prediction)
                # print(f'\t\t|____No-Fire')
                # cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 10)
                cv2.putText(
                    frame,
                    "No-Fire",
                    (int(width / 16), int(height / 4)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 00),
                    2,
                    cv2.LINE_AA,
                )
            else:
                # print("cul", prediction)
                # print(f'\t\t|____Fire')
                # try:
                #     os.mkdir("media/detect_image/" + cam_id)
                # except:
                #     print("An exception occurred")

                folder_path = "media/detect_image/" + cam_id

                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    print("Thư mục đã tồn tại.")
                else:
                  os.mkdir("media/detect_image/" + cam_id)
                # try:

                    # date_string = localtime.strftime("%Y-%m-%d")
                    # now = datetime.datetime.now().second

                #     # print(datestring, "cam id", cam_id)
                #     path = "media/detect_image/" + cam_id + "/" + date_string

                #     os.mkdir("media/detect_image/" + cam_id + "/" + date_string)
                # except:
                #     print("An exception occurred")
                date_string = localtime.strftime("%Y-%m-%d")
                now = datetime.datetime.now().second
                path = "media/detect_image/" + cam_id + "/" + date_string
                if os.path.exists(path) and os.path.isdir(path):
                    print("Thư mục đã tồn tại.")
                else:
                  os.mkdir(path)    

                today = datetime.datetime.now()
                # print(today.strftime("%Y-%m-%d"))

                # if int(localtime.second) % 2 == 0:
                if (now != end) & (int(now - end) % 5 == 0):
                    # print("time end",end)
                    # print(str(threading.current_thread().ident) + " Phat hien chay " + str(today))
                    cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 30)
                    out_path = "media/detect_image/" + cam_id + "/" + date_string
                    date_full = localtime.strftime("%Y-%m-%d %H:%M")
                    localtime.strftime("%d %H-%M-%S")
                    frame_name = localtime.strftime("%d %H-%M-%S") + ".jpg"
                    cv2.imwrite(os.path.join(out_path, frame_name), frame)
                    name = "Phat hien chay"
                    content = "co dam chay"
                   
                    print("===========================",date_full )
                    end = datetime.datetime.now().second
                    dec = Detection.objects.create(
                        name_detect=name,
                        name_cam=cam_id,
                        content=content,
                        image_detect="detect_image/"
                        + cam_id
                        + "/"
                        + date_string
                        + "/"
                        + frame_name,
                        time_detect=date_full,
        
                    )
                    dec.save()

                cv2.putText(
                    frame,
                    "Fire",
                    (int(width / 16), int(height / 4)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            time_now = time.time()
            total_time += time_now - time_start
            fps = num_frames / total_time
            # uncomment below to see FPS of camera stream\

            cv2.putText(
                frame,
                "FPS: %.2f" % fps,
                (int(20), int(40 * 5e-3 * frame.shape[0])),
                0,
                2e-3 * frame.shape[0],
                (255, 255, 255),
                2,
            )

            yield cam_id, frame, prediction
