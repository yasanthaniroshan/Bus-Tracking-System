from django.urls import path
from . import views

urlpatterns = [
    path('',views.iotdevice,name="webhook")
]
