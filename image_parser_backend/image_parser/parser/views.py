import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from parser.models import Image
from parser.encoders import ImageEncoder
from parser.parseAPI import parse_images
import requests
from PIL import Image as Imagge

from serpapi import GoogleSearch


def index(request):
    return HttpResponse("Базовая страница")


def parse(request):
    query = request.GET.get("query")
    if query == "":
        return JsonResponse({"message": "Bad request"}, status=400)
    if len(Image.objects.filter(name=query)) == 0:
        parse_images(query)
        return JsonResponse({"message": "success"}, status=200)
    return JsonResponse({"message": "success"}, status=200)


def get_one(request):
    query = request.GET.get("query")
    images = Image.objects.filter(is_accepted=False, name=query)
    if not images.exists():
        return JsonResponse({"message": "Bad request"}, status=400)
    return JsonResponse({"body": images[0], "message": "success"}, status=200, safe=False, encoder=ImageEncoder)


def accept(request):
    idx = request.GET.get("id")
    image = Image.objects.get(pk=idx)
    if not image:
        return JsonResponse({"message": "Doesn't exist"}, status=400)
    image.is_accepted = True
    image.save()
    return JsonResponse({"message": "success"}, status=200)


def reject(request):
    idx = request.GET.get("id")
    image = Image.objects.get(pk=idx)
    if not image:
        return JsonResponse({"message": "Doesn't exist"}, status=400)
    image.delete()
    return JsonResponse({"message": "success"}, status=200)


def get_next(request):
    image = Image.objects.filter(is_accepted=True)[0]
    if not image:
        return JsonResponse({"message": "Doesn't exist"}, status=400)
    return JsonResponse({"body": image, "message": "success"}, status=200, safe=False, encoder=ImageEncoder)


def download(request):

    url = request.GET.get("url")
    idx = request.GET.get("id")
    img = requests.get(url)
    if not img:
        return JsonResponse({"message": "Bad request"}, status=400)
    try:
        Image.objects.get(pk=idx).delete()
        with open("images/img" + str(idx) + ".jpg", "wb") as file:
            file.write(img.content)
    except Exception:
        return JsonResponse({"message": "Bad request"}, status=400)
    return JsonResponse({"message": "success"}, status=200)


def trim(request):
    idx = request.GET.get("id")
    if not idx:
        return JsonResponse({"message": "Bad request"}, status=400)
    x = int(request.GET.get("x"))
    y = int(request.GET.get("y"))
    width = int(request.GET.get("width"))
    height = int(request.GET.get("height"))
    img = Imagge.open("images/img"+str(idx)+".jpg")
    im_crop = img.crop((x, y, x+width, y+height))
    im_crop.save("images/img"+str(idx)+".jpg", quality=95)
    return JsonResponse({"message": "success"}, status=200)

