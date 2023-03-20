"""kush_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from beacons import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("static", views.open_static_landing_page, name="open_static"),
    path("static_qr_code", views.generate_static_qr_code, name="static_qr_code"),
    path("dyanamic", views.open_dynamic_landing_page, name="open_dynamic"),
    path("dynamic_qr_code", views.generate_dynamic_qr_code, name="dynamic_qr_code"),
    path("travel", views.open_travel_landing_page, name="travel_landing_page"),
    path("travel_doc_qr_code", views.travel_documents_qr_code, name="travel_documents_qr_code"),
    path("v_card_qr_code", views.v_card_qr_code, name="v_card_qr_code"),
    path("sms_qr_code", views.sms_qr_code, name="sms_qr_code"),
    path("email_qr_code", views.email_qr_code, name="email_qr_code")
]
