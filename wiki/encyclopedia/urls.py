from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<selection>/",views.entry,name="entry"),
    path("wiki/<selection>/",views.entry,name="entry"),
    path("edit/<selection>/",views.edit,name="edit"),
    path("new",views.new,name="new"),
    path("search",views.search,name="search")
]
