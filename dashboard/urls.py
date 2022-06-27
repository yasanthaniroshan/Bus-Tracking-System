from django.urls import path
from . import views

urlpatterns = [
    path('<str:bus_id>',views.tourdashboard,name="tour")
]
