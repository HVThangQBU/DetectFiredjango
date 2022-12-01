
import cv2
import time
from canhbao.detectionfire import CameraDetectionFire
from canhbao.base_camera import BaseCamera



class Camera(BaseCamera):

    def __init__(self, feed_type, device, port_list):
        super(Camera, self).__init__(feed_type, device, port_list)

    @staticmethod
    def server_frames(image_hub):
        num_frames = 0
        total_time = 0
        while True:  # main loop
            time_start = time.time()

            cam_id, frame = image_hub.recv_image()

            image_hub.send_reply(b'OK')  # this is needed for the stream to work with REQ/REP pattern

            print("camera ID", cam_id)
            num_frames += 1
            # detection fire
            Test = CameraDetectionFire()
            frame = Test.dectection_fire(frame, cam_id)

            time_now = time.time()
            total_time += time_now - time_start
            fps = num_frames / total_time
                      # uncomment below to see FPS of camera stream
            cv2.putText(frame, "FPS: %.2f" % fps, (int(20), int(40 * 5e-3 * frame.shape[0])), 0, 2e-3 * frame.shape[0],(255, 255, 255), 2)


            yield cam_id, frame
