from django.urls import re_path

from bot import views


urlpatterns = [
    re_path(r'^verify?$', views.VerView.as_view()),
]