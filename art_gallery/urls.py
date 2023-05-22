from django.urls import path
from art_gallery import views

urlpatterns = [
    path("", views.home, name="home"),
]