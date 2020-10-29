from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_title, name="title"),
    path("search", views.search, name="search"),
    path("add", views.add_page, name="add"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("random", views.random_page, name="random")
]
