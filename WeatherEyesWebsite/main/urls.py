from django.urls import path

from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("v1/", views.v1, name="view 1"),
    path("future_forecast/", views.future_forecast, name="future forecast"),
    path("observational_inquiry/", views.observational_inquiry, name="observational inquiry"),
    path("preferences/", views.preferences, name="preferences"),
    path('current_forecast', views.current_forecast, name='current_forecast'),
]
