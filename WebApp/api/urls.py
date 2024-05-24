from django.urls import path
from webhook.views import ActiveOrDisconnected

urlpatterns = [
    path('js/',ActiveOrDisconnected,name="Status")
]