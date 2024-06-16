
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.chat_view, name="chat_view"),
    path('send-message/', views.send_message, name='send_message'),
]
