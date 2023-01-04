import cv2
from PIL import Image
import time
import yaml
import torch
import os
import datetime
import torchvision.transforms as transforms
from canhbao.models import shufflenetv2
from canhbao.models.models import Detection
import threading


class CameraDetectionFire(object):
  def __init__(self):
    pass
  def data_transform(self, model):
    # transforms needed for shufflenetonfire
    if model == 'shufflenetonfire':
      np_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
      ])
    # transforms needed for nasnetonfire
    if model == 'nasnetonfire':
      np_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
      ])

    return np_transforms

  ##########################################################################

    # read/process image and apply tranformation

  def read_img(self, frame, np_transforms):
    small_frame = cv2.resize(frame, (224, 224), cv2.INTER_AREA)
    small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    small_frame = Image.fromarray(small_frame)
    small_frame = np_transforms(small_frame).float()
    small_frame = small_frame.unsqueeze(0)
    small_frame = small_frame.to(device)

    return small_frame

  ##########################################################################

  # model prediction on image
  def run_model_img(self, args, frame, model):
    output = model(frame)
    pred = torch.round(torch.sigmoid(output))
    print(torch.sigmoid(output))
    return pred

  ##########################################################################

  # drawing prediction on image
  # def draw_pred(self,args, frame, pred, fps_frame):
  #   height, width, _ = frame.shape
  #   if prediction == 1:
  #     if args["image"] or args["webcam"]:
  #       print(f'\t\t|____No-Fire | fps {fps_frame}')
  #     cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 2)
  #     cv2.putText(frame, 'No-Fire', (int(width / 16), int(height / 4)),
  #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
  #   else:
  #     if args["image"] or args["webcam"]:
  #       print(f'\t\t|____Fire | fps {fps_frame}')
  #     cv2.rectangle(frame, (0, 0), (width, height), (0, 255, 0), 2)
  #     cv2.putText(frame, 'Fire', (int(width / 16), int(height / 4)),
  #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
  #   return frame

  def dectection_fire(self, frame):
    with open('canhbao/config.yml') as f:
      config = yaml.load(f, Loader=yaml.FullLoader)
    args = config
    global device
    WINDOW_NAME = 'Detection'
    if args["cpu"]:
        device = torch.device('cpu')
    else:
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    if args["cpu"] and args["trt"]:
        print(f'\n>>>>TensorRT runs only on gpu. Exit.')
        exit()

    print('\n\nBegin {fire, no-fire} classification :')

    # model load
    if args["models"]["md1"] == "shufflenetonfire":
        model = shufflenetv2.shufflenet_v2_x0_5(
            pretrained=False, layers=[
                4, 8, 4], output_channels=[
                24, 48, 96, 192, 64], num_classes=1)
        if args["weight"]:
            w_path = args["weight"]
        else:
            w_path = 'canhbao/weights/shufflenet_ff.pt'
        model.load_state_dict(torch.load(w_path, map_location=device))
    else:
        print('Invalid Model.')
        exit()

    # apply data transform
    np_transforms = self.data_transform(args["models"]["md1"])

    print(f'|__Model loading: {args["models"]["md1"]}')

    model.eval()
    model.to(device)

    fps = []
    start_t = time.time()
    small_frame = self.read_img(frame, np_transforms)

    # model prediction
    prediction = self.run_model_img(args, small_frame, model)

    stop_t = time.time()
    fps_frame = int(1 / (stop_t - start_t))
    fps.append(fps_frame)

    # drawing prediction output

    sum = 0
    localtime = datetime.datetime.now()
    #localtime = time.localtime(time.time())





      # path = r'D:/PYCHARM/DetectionFireflash/image/img'
      # # os.chdir(directory)
      # cv2.imwrite(path + str(num) + ".jpg", frame)
      # chatId = 5150505079
      # text = "test telegram"
      # photo = open(path + str(num) + ".jpg", "rb");
      # to = "hoangthangddt870@gmail.com"
      # print("tong ", num)
      # caption = "co su co !" + path + str(num) + ".jpg"
      # thu = SendWarning()
      # thu.sendEmail(to, photo)
      # #thu.sendTelegram(chatId, text, photo, caption)

    return prediction,frame




































