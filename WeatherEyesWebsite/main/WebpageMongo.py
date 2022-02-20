import pymongo
from pymongo import MongoClient
import pprint
import datetime
from datetime import date

class WebpageMongo:

    def __init__(self):
        self.dates = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dev']
        self.client = pymongo.MongoClient("mongodb+srv://team:team@cluster0.yknbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def Single_Day_Inquriy_Obs(self, date, collection, userid):
        new_date = date[0]+date[1]+date[2]
        results = collection.find({"Date": new_date})
        for x in results:
            High = x['HighTempF']
            Low = x['LowTempF']
            Rain = x['Rainfall']
            Snow = x['Snowfall']
        WDate = date[0] + " " + date[1] + " " + date[2]
        Webreturn = {"Date" : WDate , "High" : High , "Low" : Low , "Rainfall" : Rain , "Snowfall" : Snow}
        return Webreturn

    def Single_Day_Inquiry_Hourly_Obs(self,date, collection, userid):
        Date = date[0] + date[1] + date[2]
        time = self.time_convert(date[3], date[4])
        results = collection.find({"Date":Date, "Time": time})
        for x in results:
            Temp = x['TemperatureF']
            if x['Precipitation'] == 'No precipitation':
                Rainfall = "No Precipitation"
            else:
                Rainfall = x['Precipitation']
        time_per =  date[0] + " " + date[1] + " " + date[2] + " " + time
        Webreturn = {"Date" : time_per , "Temp" : Temp , "Rainfall" : Rainfall}
        return Webreturn

    def Interval_Inquiry_Hourly_Obs(self, date, collection, userid):
        start_date = date[0] + date[1] + date[2]
        start_time = self.time_convert(date[3], date[4])
        end_date = date[6] + date[7] + date[8]
        end_time = self.time_convert(date[9], date[10])
        temps = []
        rain = []
        delta = datetime.timedelta(days = 1)
        start = datetime.date(int(date[2]), self.recodedate_num(start_date[:3]), int(date[1]))
        end = datetime.date(int(date[8]), self.recodedate_num(end_date[:3]), int(date[7]))
        while start <= end:
            year = start.strftime('%Y')
            month = self.recodedate_str(start.strftime('%m'))
            day = start.strftime('%d')
            search_date = month + day + year
            switch = 0
            while switch == 0:
                results = collection.find({"Date":search_date, "Time": start_time})
                for x in results:
                    temps.append(float(x['TemperatureF']))
                    if type(x['Precipitation']) == float or x['Precipitation'].isdigit():
                        rain.append(float(x['Precipitation']))
                start_time = self.iterate_time(start_time)
                if start_time == "1:00AM":
                    switch = 1
            switch = 0
            start = start + delta
        start = start_date + " " + start_time
        end = end_date + " " + end_time
        high = max(temps)
        low = min(temps)
        Totalrain = sum(rain) #change units to user pref
        Webreturn = {"Start" : start , "End" : end , "MaxTemp" : high , "MinTemp" : low , "Rainfall" : Totalrain}
        return Webreturn

    def Interval_Inquiry(self, start_date, end_date, collection, userid):
        start = date(int(start_date[2]), self.recodedate_num(start_date[0]), int(start_date[1]))
        end = date(int(end_date[2]), self.recodedate_num(end_date[0]), int(end_date[1]))
        delta = datetime.timedelta(days = 1)
        temps = []
        snow = []
        rain = []
        while start <= end:
            year = start.strftime('%Y')
            month = self.recodedate_str(start.strftime('%m'))
            day = start.strftime('%d')
            new_date = month+day+year
            results = collection.find({"Date": new_date})
            for x in results:
                temps.append(float(x['HighTempF']))
                temps.append(float(x['LowTempF']))
                if type(x['Rainfall']) == float or x['Rainfall'].isdigit():
                    rain.append(float(x['Rainfall'])) #change units to user pref
                if type(x['Snowfall']) == float or x['Snowfall'].isdigit():
                    snow.append(float(x['Snowfall'])) #change units to user pref
            start = start + delta
        high = max(temps) #Will eventually code to user preference
        low = min(temps) #Will eventually code to user preference
        Totalsnow = sum(snow) #change units to user pref
        Totalrain = sum(rain) #change units to user pref
        Webreturn = {"Start" : start_date , "End" : end_date , "MaxTemp" : high , "MinTemp" : low , "Snowfall" : Totalsnow , "Rainfall" : Totalrain}
        return Webreturn

    def Forecast_Inquiry(self, date, time, service_prov, timeinterval):
        db = self.client[service_prov]
        if timeinterval == "daily":
            if service_prov == "NatWeather":
                period = "sevenday"
            if service_prov == "AccuWeather" or service_prov == "WeatherCom":
                period = "tenday"
        if timeinterval == "hourly":
            period = "hourly"
        collection_name = service_prov + "_" + period
        collection = db[collection_name]
        date = date.split()
        date = date[0] + date[1] + date[2]
        timeCollected = date + " " + time
        results = collection.find({"TimeCollected": timeCollected})
        Dates = [] ; Precip = [] ; Descrip = [] ; MinTemp = [] ; MaxTemp = [] ; Temp = [] ; Listionary = []; Hours = []
        if timeinterval == "daily":
            for x in results:
                newFormatDate = x["Date"][0:3] + " " + x["Date"][3:5] + ", " + x["Date"][5:]
                # print(newFormatDate)
                Dates.append(newFormatDate)
                Precip.append(x["PrecipitationProb"])
                Descrip.append(x["Description"])
                MinTemp.append(x["MinTempF"]) #Will eventually code to user preference
                MaxTemp.append(x["MaxTempF"]) #Will eventually code to user preference
                Docs = {"Date" : newFormatDate, "Precipitation_Probability" : x["PrecipitationProb"] , "Description" : x["Description"], "MinTemp" : x["MinTempF"], "MaxTemp" : x["MaxTempF"]} # Will eventually code to user preference
                Listionary.append(Docs)
            return Listionary
        if timeinterval == "hourly":
            if service_prov == "AccuWeather":
                for x in results:
                    Hours.append(x["Hour"])
                    Precip.append(x["PrecipitationProb"])
                    Temp.append(x["TemperatureF"]) #Will code to user preference
                    Descrip.append(x["Description"])
                    Docs = {"Hour" : x["Hour"], "Precipitation_Probability" : x["PrecipitationProb"], "Description" : x["Description"], "Temperature" : x["TemperatureF"]}
                    Listionary.append(Docs)
                return Listionary
            if service_prov == "NatWeather":
                for x in results:
                    Hours.append(x["Hour"])
                    Descrip.append(x["Description"])
                    Temp.append(x["TemperatureF"]) #Will code to user preference
                    Docs = {"Hour": x["Hour"], "Description" : x["Description"], "Temperature" : x["TemperatureF"]}
                    Listionary.append(Docs)
                return Listionary
            if service_prov == "WeatherCom":
                for x in results:
                    Hours.append(x["Hour"])
                    Descrip.append(x["Description"])
                    Temp.append(x["TemperatureF"]) #Will code to user preference
                    Precip.append(x["PrecipitationProb"])
                    Docs = {"Hour" : x["Hour"], "Precipitation_Probability" : x["PrecipitationProb"], "Description" : x["Description"], "Temperature" : x["TemperatureF"]}
                    Listionary.append(Docs)
                return Listionary
        return Listionary


    def Current_Forecast(self):
        date = datetime.datetime.now().strftime("%b %d %Y")
        time = datetime.datetime.now().strftime("%I%p")
        ah = self.Forecast_Inquiry(date, time, "AccuWeather", "hourly")
        # print("ah original")
        # print(ah)
        # if (ah == []):
        #     lastHourDateTime = datetime.datetime.now() - datetime.timedelta(hours = 1)
        #     time = lastHourDateTime.strftime("%I%p")
        #     print(time)
        #     ah = self.Forecast_Inquiry(date, time, "AccuWeather", "hourly")
        #     print("ah past")
        #     print(ah)
        #
        # date = datetime.datetime.now().strftime("%b %d %Y")
        # time = datetime.datetime.now().strftime("%I%p")
        ad = self.Forecast_Inquiry(date, time, "AccuWeather", "daily")
        # print("ad original")
        # print(ad)
        if (ad == []):
            lastHourDateTime = datetime.datetime.now() - datetime.timedelta(hours = 1)
            time = lastHourDateTime.strftime("%I%p")
            print(time)
            ah = self.Forecast_Inquiry(date, time, "AccuWeather", "daily")
            # print("ad past")
            # print(ad)
        #
        date = datetime.datetime.now().strftime("%b %d %Y")
        time = datetime.datetime.now().strftime("%I%p")
        nh = self.Forecast_Inquiry(date, time[1:], "NatWeather", "hourly")
        # print("nh original")
        # print(nh)
        # if (nh == []):
        #     lastHourDateTime = datetime.datetime.now() - datetime.timedelta(hours = 1)
        #     time = lastHourDateTime.strftime("%I%p")
        #     print(time)
        #     nh = self.Forecast_Inquiry(date, time, "NatWeather", "hourly")
        #     print("nh past")
        #     print(nh)

        # date = datetime.datetime.now().strftime("%b %d %Y")
        # time = datetime.datetime.now().strftime("%I%p")
        nd = self.Forecast_Inquiry(date, time[1:], "NatWeather", "daily")
        # if (nd == []):
        #     lastHourDateTime = datetime.datetime.now() - datetime.timedelta(hours = 1)
        #     time = lastHourDateTime.strftime("%I%p")
        #     nd = self.Forecast_Inquiry(date, time, "NatWeather", "daily")
        wh = self.Forecast_Inquiry(date, time, "WeatherCom", "hourly")
        # print(wh)
        wd = self.Forecast_Inquiry(date, time, "WeatherCom", "daily")
        # print(wd)
        return [ah, ad, nh, nd, wh, wd]

    def recodedate_str(self, date):
        """This method takes a numerical month and returns the actual name of the month as a string"""
        recoding_str = {
            '01' : 'Jan',
            '02' : 'Feb',
            '03' : 'Mar',
            '04' : 'Apr',
            '05' : 'May',
            '06' : 'Jun',
            '07' : 'Jul',
            '08' : 'Aug',
            '09' : 'Sep',
            '10': 'Oct',
            '11' : 'Nov',
            '12': 'Dec',
            }
        return recoding_str[date]

    def time_convert(self, time, ampm):
        """
        This method converts times into the format stored in mongodb from weather.gov. It is passed
        the time to convert and whether the time is in AM or PM
        """
        time = str(time) + ":00"
        if ampm == 'AM':
            time = str(time) + "AM"
        if ampm == 'PM':
            time = str(time) + "PM"
        return time

    def iterate_time(self, time):
        """
        This method is passed a time to increase by an hour. For instance 1 AM becomes 2 AM, 12 PM becomes
        1 AM.
        """
        if len(time) == 6:
            ampm = time[4:]
            lead = int(time[0])
        if len(time) == 7:
            ampm = time[5:]
            lead = int(time[0:2])
        lead = lead + 1
        if lead == 13:
            lead = 1
            if ampm == "AM":
                ampm = "PM"
            else:
                ampm = "AM"
        time = str(lead) + ":00" + ampm
        return str(time)

    def main(self):
        self.Current_Forecast()
