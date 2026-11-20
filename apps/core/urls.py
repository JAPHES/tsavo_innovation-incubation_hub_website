from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("programmes-events/", views.programmes_events, name="programmes_events"),
    path("partnerships/", views.partnerships, name="partnerships"),
    path("robots.txt", views.robots_txt, name="robots"),
]
