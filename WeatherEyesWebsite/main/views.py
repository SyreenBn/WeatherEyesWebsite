from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .WebpageMongo import WebpageMongo

unit = 'C'
datatype = 'Daily'

# Create your views here.
def index(response):
    return render(response, "main/base.html", {})

#This is just a test view
def v1(response):
    return HttpResponse("<h1>View 1</h1>")

def home(response):
    return render(response, "main/home.html", {})

def future_forecast(response):
    return render(response, "main/future_forecast.html", {})

def preferences(response):
    return render(response, "main/preferences.html", {})

def observational_inquiry(response):
    return render(response, "main/observational_inquiry.html", {})

def current_forecast(response):
    WM = WebpageMongo()
    data = WM.Current_Forecast()
    ah = data[0]
    ad = data[1]
    nh = data[2]
    nd = data [3]
    wh = data[4]
    wd = data[5]
    # print(wh,wd)

    return render(response, "main/current_forecast.html", {

        'unit': unit,
        'datatype':datatype,

        'WeatherComDailyData': wd,
        'WeatherComHourlyData': wh,
        #
        'AccuWeatherDailyData': ad,
        'AccuWeatherHourlyData': ah,
        #
        'NatWeatherDailyData': nd,
        'NatWeatherHourlyData': nh
        })
