from http import HTTPStatus

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import urls
from . import constants
import requests


def generate_static_qr_code(org_id, custom_url, qr_type, location=False):
    url = "https://api.beaconstac.com/api/2.0/qrcodes/"
    print(url)
    headers = {
        "Authorization": f"Token {constants.MY_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "name": "Custom URL",
        "organization": 281387,
        "qr_type": 1,
        "fields_data": {
            "qr_type": 1,
            "url": custom_url
        },
        "campaign": {
            "content_type": 1,
            "custom_url": custom_url
        },
        "location_enabled": location,
        "attributes": {
            "color": "#2595ff",
            "colorDark": "#2595ff",
            "margin": 80,
            "isVCard": False,
            "frameText": "BEACONSTAC",
            "logoImage": "https://d1bqobzsowu5wu.cloudfront.net/15406/36caec11f02d460aad0604fa26799c50",
            "logoScale": 0.1992,
            "frameColor": "#2595FF",
            "frameStyle": "banner-bottom",
            "logoMargin": 10,
            "dataPattern": "square",
            "eyeBallShape": "circle",
            "gradientType": "none",
            "eyeFrameColor": "#2595FF",
            "eyeFrameShape": "rounded"
        }
    }
    response = requests.post(url=url, headers=headers, json=body)
    print(response.status_code)
    if response.status_code == 201:
        print(response.json()["id"])
        return response
    else:
        print(response.text, response.json(), response)

        return response


def download_staic_qr_code(id, type="jpeg"):
    pre = "https://api.beaconstac.com/api/2.0/qrcodes/"
    url = f"{pre}/{str(id)}/download?size = 1024 & error_correction_level = 5 & canvas_type = {type}"
    print("id, url     ",id,url,pre)
    headers = {
        "Authorization": f"Token {constants.MY_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print()
        return response
    else:
        print(response.text)
        return response

