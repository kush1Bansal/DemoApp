import base64
import os
import uuid
from datetime import datetime
from http import HTTPStatus

from django.contrib.sites import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .api_collections import static_qr
from .api_collections import dynamic_qr
from django.views.decorators.http import require_POST
import requests
import pyperclip


def index(request):
    return render(request, "base.html")


def download_static_qr_code(response):
    print("enter download")
    print(response)
    data = response.json()
    id = data.get("id")
    if not id:
        return JsonResponse({'status': 'QR Code not generated'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    print(id)
    type = data.get("type")
    response = static_qr.download_staic_qr_code(id, type)
    if response.status_code == 200:
        print("qr downloaded successfully")
        return response
    else:
        return JsonResponse({'status': 'Error Downloading'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def generate_static_qr_code(request):
    print("yoyoyoyoyoyooyoy")
    try:
        data = request.POST
        org_id = data.get("org_id")
        print(data)
        if not org_id:
            org_id = 281387
            # return JsonResponse({'status': 'Organisation Id cannot be null'}, status=HTTPStatus.BAD_REQUEST)

        custom_url = data.get("custom_url")
        print(custom_url)
        qr_type = 1

        response = static_qr.generate_static_qr_code(org_id=org_id, custom_url=custom_url, qr_type=qr_type)

        if response.status_code == 201:
            print("api request succesful")
            res = download_static_qr_code(response)
            d = res.json()
            url = d.get("urls")["png"]
            print("url", url)
            context = {"url": url}
            return render(request, "static_qr.html", context=context)

        else:
            return JsonResponse({'status': 'Error Generating QR Code'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    except Exception as e:
        return JsonResponse({'status': e}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def open_dynamic_landing_page(request):
    return render(request, "dynamic.html")


def open_static_landing_page(request):
    return render(request, "static.html")


def open_travel_landing_page(request):
    return render(request, "travel.html")


def download_dynamic_qr_code(response):
    print("enter download dynamic")
    print(response, response.json())
    data = response.json()
    id = data.get("id")
    if not id:
        return JsonResponse({'status': 'QR Code not generated'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    print(id)
    type = data.get("type")
    response = dynamic_qr.download_dynamic_qr_code(id, type)
    if response.status_code == 200:
        print("dynamic qr downloaded successfully")
        return response
    else:
        return JsonResponse({'status': 'Error Downloading'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def generate_dynamic_qr_code(request):
    try:
        print("i am here")
        data = request.POST
        print(data)
        org_id = data.get("org_id")
        if not org_id:
            org_id = 11181

        id = data.get("id")
        action_type = data.get("action")
        print("action_type", action_type, type(action_type))
        if action_type == "15":
            phone = data.get("phone")
            country_code = data.get("country_code")
            phone_number = f"+{country_code} {phone}"
            print("fhfhfhfhfhfhfhffhfhfhhff", phone_number)
            qr_type = 2

            response = dynamic_qr.phone_call_qr(org_id=org_id, phone_number=phone_number, qr_type=2)
        if response.status_code == 201:
            print("api request succesful")
            res = download_dynamic_qr_code(response)
            d = res.json()
            url = d.get("urls")["jpeg"]
            print("url", url)
            context = {"url": url, "render_qr": True}
            return render(request, "dynamic.html", context=context)
        else:
            return JsonResponse({'status': 'Error Generating QR Code'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    except Exception as e:
        return JsonResponse({'status': e}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def upload_file(request, file):
    import requests
    import json
    # content = base64.b64encode(file.read())
    # content = base64.b64encode(file.read())
    # content = base64.b64encode(file.read().encode('utf-8')).decode('utf-8')
    content = str(base64.b64encode(file.read()))

    pyperclip.copy(content)
    url = f"https://api.github.com/repos/kush1101/task-manager-app/contents/gov_id_{datetime.now()}"

    payload = json.dumps({
        "message": "my commit message",
        "committer": {
            "name": "kushagra",
            "email": "kushagrabansalajmer@gmail.com"
        },
        "content": f"{content[2:-1]}"
    })
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    print("sent iupload request")
    print("response", response.json(), response.status_code)
    if response.ok:
        print("responded here")
        file_url = response.json()['content']['html_url']
        return file_url
    else:
        return


def travel_documents_qr_code(request):
    print("GFHGFGFHFHF")
    print(request.FILES)
    gov_id = request.FILES['gov_id']
    flight_ticket = request.FILES["flight_ticket"]
    url1 = upload_file(request, gov_id)
    url2 = upload_file(request, flight_ticket)

    response = dynamic_qr.travel_pdf_qr_code(url1, url2)
    if response.status_code == 201:
        print("api request succesful")
        res = download_dynamic_qr_code(response)
        if res.status_code == 200:
            d = res.json()
            url = d.get("urls")["jpeg"]
            print("url", url)
            context = {"url": url, "render_qr": True}
            return render(request, "travel.html", context=context)
        else:
            return JsonResponse({'status': 'Error Generating QR Code'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({'status': 'Error Generating QR Code'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def v_card_qr_code(request):
    data = request.POST

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    company = data.get("company")
    email = data.get("email")
    designation = data.get("designation")
    work_phone = data.get("work_phone")
    home_phone = data.get("home_phone")
    state = data.get("state")
    country = data.get("country")

    phone = {"work_phone": work_phone, "home": home_phone}
    resp = dynamic_qr.v_card_qr_code(first_name=first_name, last_name=last_name, company=company, email=email,
                                     designation=designation, phone=phone, state=state, country=country)

    if resp.status_code == 200:
        d = resp.json()
        url = d.get("urls")["jpeg"]
        context = {"url": url, "render_qr": True}
        return render(request, "dynamic.html", context=context)
    return JsonResponse({'status': 'Error Generating QR Code'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
