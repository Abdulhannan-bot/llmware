from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('chat',views.prompt_with_sources_basic, name="chat")
]