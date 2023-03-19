from http import HTTPStatus

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import urls
from . import constants
import requests, json


def phone_call_qr(org_id, phone_number, qr_type=2, content_type=15):
    url = "https://beaconstacqa.mobstac.com/api/2.0/qrcodes/?organization=11181"
    # url = urls.Action_urls["GENERATE_STATIC_QR_CODE"]
    print(url, type(url))
    headers = {
        "Authorization": f"Token 441f5312d9208cd9602f7bb410a1a283164e8a53",
        "Content-Type": "application/json"
    }

    body = {
        "name": "Call by phone",
        "organization": org_id,
        "qr_type": qr_type,
        "campaign": {
            "content_type": 15,
            "phone_call": {
                "phone": phone_number
            }
        },
        "location_enabled": False,
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
        return response
    else:
        print(response.json())
        return response


def download_dynamic_qr_code(id, type="jpeg"):
    url = f"https://beaconstacqa.mobstac.com/api/2.0/qrcodes/{id}/download/?size=1024&error_correction_level=5" \
          f"&canvas_type=jpeg"
    print(id)
    headers = {
        "Authorization": f"Token 441f5312d9208cd9602f7bb410a1a283164e8a53",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("download function call success")
        return response

    else:
        print(response.text)
        return response


def v_card_qr_code(first_name, last_name, company, email, designation, phone: dict, state, country="India",
                   address_url=None):
    url = "https://beaconstacqa.mobstac.com/api/2.0/qrcodes/?organization=11181"

    payload = json.dumps({
        "name": "vCard Plus QR Code",
        "organization": 11181,
        "qr_type": 2,
        "campaign": {
            "content_type": 7,
            "vcard_plus": {
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "designation": designation,
                "email": email,
                "phone": {
                    "home": phone.get("home"),
                    "work": phone.get("work"),
                    "mobile": phone.get("mobile")
                },
                "state": state,
                "country": country,
                "address_url": url
            }
        }
    })
    headers = {
        'Authorization': 'Token 441f5312d9208cd9602f7bb410a1a283164e8a53',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
        print("v card successfully created")
        id = response.json().get("id")
        final_resp = download_dynamic_qr_code(id)
        print("final resp", final_resp.json(),final_resp.status_code)
        if final_resp.status_code == 200:
            return final_resp
        else:
            return JsonResponse({'status': 'Error downloading V card qr Code'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        JsonResponse({'status': 'Error Generating V card'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

def travel_pdf_qr_code(url1,url2):
    url = "https://beaconstacqa.mobstac.com/api/2.0/qrcodes/?organization=11181"

    payload = json.dumps({
        "name": "PDF",
        "organization": 11181,
        "qr_type": 2,
        "campaign": {
            "content_type": 13,
            "pdf": {
                "name": "Beaconstac QR Code solution",
                "files": [
                    {
                        "url": url1,
                        "name": "Government ID"
                    },
                    [
                        {
                            "url": url2,
                            "name": "boarding_pass"
                        }
                    ]

                ],
                "uploaded": True
            }
        },
        "location_enabled": False,
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
    })
    headers = {
        'Authorization': 'Token 441f5312d9208cd9602f7bb410a1a283164e8a53',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response
