"""finnc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from dashboard.views import frontpage,gettinglocations,tourdetails,survey,avaialableshedules

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/',include("webhook.urls")),
    path('dashboard/',include("dashboard.urls")),
    path('api/',include('api.urls')),
    path('',frontpage,name="frontpage"),
    path('location/',gettinglocations,name="location"),
    path('available-shedules/<int:tour_id>',avaialableshedules,name="available-shedules"),
    path('tour-details/<int:tour_id_with_number>',tourdetails,name="tourdetails"),
    path('survey/',survey,name="survey"),
    # path('bus-details/<str:bus_id>',)
]
