from django.urls import path

from . import views

urlpatterns = [
    path("put-link/", views.PutLinkView.as_view()),
]
