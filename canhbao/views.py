import json
from pyexpat.errors import messages
import time
from importlib import import_module
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
import cv2
from django.db import connection
from django.http import HttpResponse, StreamingHttpResponse
from django.http.response import JsonResponse
from django.template import loader
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from canhbao.models.models import Camera, Detection, CustomUser
from django.forms.models import model_to_dict
from django.http import HttpResponseNotFound, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from canhbao.serializers import CameraSerializer


@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    print("ten", user_object)
    allcam = Camera.objects.all().values()
    template = loader.get_template("home.html")
    context = {
        "allcam": allcam,
        "user_object": user_object,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="signin")
def detailCamera(request, id):
    template = loader.get_template("detail-camera.html")
    print("id chi so: ", id)
    queryset = Camera.objects.all()
    id_cam = queryset[id].id_cam

    camera = Camera.objects.get(id_cam=id_cam)
    # detect = Detection.objects.get(name_cam=camera.name_cam)
    # detect_last = (
    #     Detection.objects.filter(name_cam=camera.name_cam)
    #     .order_by("-time_detect")
    #     .values()[1]
    # )
    detect_last = (
        Detection.objects.filter(name_cam=camera.name_cam)
        .order_by("-id_detect")
        .first()
    )

    # detect = (
    #     Detection.objects.filter(name_cam=camera.name_cam)
    #     .order_by("-time_detect")
    #     .values()[:20:-1]
    # )
    detect = (
        Detection.objects.filter(name_cam=camera.name_cam)
        .order_by("-id_detect")
        .values()[:20]
    )
    cursor = connection.cursor()
    cursor.execute(
        'select distinct y.time_detect1 from (select  DATE_FORMAT(time_detect, "%d-%m-%Y") as  time_detect1, time_detect from canhbao_detection)  as y order by y.time_detect desc limit 10'
    )

    user_object = User.objects.get(username=request.user.username)
    context = {
        "index_cam": id,
        "camera": camera,
        "detect": detect,
        "detect_last": detect_last,
        "cursor": cursor,
        "user_object":user_object,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='signin')
def detailHistory(request, id):
    template = loader.get_template("detail-history.html")
    print("id chi so: ", id)
    queryset = Camera.objects.all()
    id_cam = queryset[id].id_cam
    camera = Camera.objects.get(id_cam=id_cam)
    # detect = Detection.objects.get(name_cam=camera.name_cam)
    detect_last = (
        Detection.objects.filter(name_cam=camera.name_cam)
        .order_by("-id_detect")
        .first()
    )


    detect = (
        Detection.objects.filter(name_cam=camera.name_cam)
        .order_by("-id_detect").values()[:20]
    )
    cursor = connection.cursor()
    cursor.execute(
        'select distinct y.time_detect1 from (select  DATE_FORMAT(time_detect, "%d-%m-%Y") as  time_detect1, time_detect from canhbao_detection)  as y order by y.time_detect desc limit 10'
    )
    user_object = User.objects.get(username=request.user.username)
    context = {
        "camera": camera,
        "detect": detect,
        "detect_last": detect_last,
        "cursor": cursor,
        "user_object":user_object,
    }

    return HttpResponse(template.render(context, request))


# @login_required(login_url='signin')
def loadDetect(request):
    id = request.GET.get("id", None)
    print("log id came", id)
    camera = Camera.objects.get(id_cam=id)
    dct = (
        Detection.objects.filter(name_cam=camera.name_cam)
        .order_by("-id_detect")
        .values()[1]
    )

    return JsonResponse({"dct": dct}, status=200)


# @login_required(login_url='signin')
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
        print("cam:", cam_id, " gen thread: ", num_frames)
        time_now = time.time()
        total_time += time_now - time_start
        fps = num_frames / total_time

        # write camera name
        cv2.putText(
            frame,
            cam_id,
            (int(0.75 * frame.shape[1]), int(0.85 * frame.shape[0])),
            0,
            1.5e-3 * frame.shape[0],
            (0, 255, 255),
            2,
        )

        # if feed_type == 'yolo':
        #     cv2.putText(frame, "FPS: %.2f" % fps, (int(0.75 * frame.shape[1]), int(0.9 * frame.shape[0])), 0,
        #                 1.5e-3 * frame.shape[0], (0, 255, 255), 2)

        frame = cv2.imencode(".jpg", frame)[
            1
        ].tobytes()  # Remove this line for test camera
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


# @login_required(login_url='signin')
def video_feed(request, feed_type, device):
    """Video streaming route. Put this in the src attribute of an img tag."""

    queryset = Camera.objects.all()
    port_list = queryset.values_list("port", flat=True)
    print(port_list)
    # port_list = (5555, 5566, 5577)
    if feed_type == "camera":
        camera_stream = import_module("canhbao.camera_server").Camera

        return StreamingHttpResponse(
            gen(
                camera_stream=camera_stream(feed_type, device, port_list),
                feed_type=feed_type,
                device=device,
            ),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )


def video_feed_one_camera(request, feed_type, device, port):
    """Video streaming route. Put this in the src attribute of an img tag."""

    # queryset = Camera.objects.all()
    # port_list = queryset.values_list('port', flat=True)
    # print(port_list)
    # port_list = (5555, 5566, 5577)
    if feed_type == "camera":
        camera_stream = import_module("canhbao.camera_server").Camera

        return StreamingHttpResponse(
            gen(
                camera_stream=camera_stream(feed_type, device, port),
                feed_type=feed_type,
                device=device,
            ),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            # messages.info(request, 'Credentials Invalid')
            return render(request, "signin.html")
    else:
        return render(request, "signin.html")


@login_required(login_url="signin/")
def logout(request):
    auth.logout(request)
    return redirect("signin")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "EMAIL TAKENS")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "USERNAME TAKENS")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                # log user in and redirectto setting page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = CustomUser.objects.create(
                    user=user_model, id_user=user_model.id
                )
                new_profile.save()
                return redirect("")
        else:
            messages.info(request, "PASS NOT MATCHING")
            return redirect("signup")
    else:
        return render(request, "signup.html")


@login_required(login_url="signin")
def mapCamera(request):
    # create a map using Mapbox GL JS
    mapbox_access_token = "pk.eyJ1IjoiYmx1ZXJoaW5vIiwiYSI6ImNqZDJjYjZxeDFzcHUzM213MGdoOTh4dXUifQ.0St02mA2vqSMM5qsvMfngQ"
    map = {
        "access_token": mapbox_access_token,
        "style": "mapbox://styles/mapbox/streets-v11",
        "center": [-122.4194, 37.7749],  # set the initial center of the map
        "zoom": 12,  # set the initial zoom level of the map
    }
    user_object = User.objects.get(username=request.user.username)
    context = {"map": map,
               "user_object": user_object,}
    template = loader.get_template("map-camera.html")
    return HttpResponse(template.render(context, request))


def get(request):
    cameras = Camera.objects.all()
    camera_list = list(cameras.values())
    return JsonResponse(camera_list, safe=False)


def search_detection(request):
    print("chua vao ",request.method)
    user_object = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        start_time = body_data.get('start_time')
        end_time = body_data.get('end_time')
        name_cam = body_data.get('name_cam')
        print("thong tin tim kiem: ",start_time," ", end_time, " ", name_cam )
        detections = Detection.objects.filter(name_cam=name_cam, time_detect__range=[start_time, end_time])
        detection_list = list(detections.values())
        return JsonResponse(detection_list, safe=False)
    else:
        # Return an HttpResponse object indicating that the request method is not supported
        return JsonResponse({}, status=400)


