from datetime import datetime
import aiohttp
import asyncio
import json
import os
from time import time, sleep
import sqlite3
from sqlite3 import Error
from pip._vendor.distlib.compat import raw_input
import myDB
from os import system

cls = lambda: system('cls')

user_api_key = os.environ['open_weather_api_key']  # access api key through window's enviroment
city_name = raw_input("Enter City Name: ")  # get city name through user
db_conn = sqlite3.connect("Weather_forecast.db")


# function to scrap url api and return a json object file
async def get_weather_forecast_async(api_key, city, session):
    """Get weather data asynchronously"""
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key
    try:
        async with session.get(url) as response:
            response_json = await response.json()
    except Exception as e:
        print("An error occurred: {}".format(e))
    return response_json


# get data our interest from the json file
def extract_data_from_response(response):
    clouds = response["weather"][0]["description"]
    temperature = response["main"]["temp"]
    wind_speed = response["wind"]["speed"]
    humidity = response["main"]["humidity"]
    city = response["name"]
    country = response["sys"]["country"]
    return city, country, clouds, temperature, wind_speed, humidity


# event loop Update data every minute
async def periodic_fetch(conn, api_key, city, session):
    """event loop Update data every minute and
        inserting return data into our db using our crud function insert from crud class
    """
    while True:
        data = await get_weather_forecast_async(api_key, city, session)  # call function that is to be refreshed
        trimmed_data = (extract_data_from_response(data))
        myDB.insert(conn, trimmed_data)
        display_weather(db_conn, "City_Weather_Data")
        await asyncio.sleep(60)



def display_weather(db_conn, table_name):
    rows = myDB.selectAllRows(db_conn, table_name)
    for row in rows:
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        print("-------------------------------------------------------------")
        print("Weather forecast for - {},{} || {}".format(rows[0][1], rows[0][2], date_time))
        print("-------------------------------------------------------------")
        print("Current temperature is: {} deg C".format(rows[0][5]))
        print("Current weather desc  :", rows[0][3])
        print("Current Humidity      :", rows[0][4], '%')
        print("Current wind speed    :", rows[0][0], 'kmph')


async def main():
    create_table_qry = ('''
                CREATE TABLE IF NOT EXISTS City_Weather_Data
                ([generate_id] INTEGER PRIMARY KEY,
                [City_Name] TEXT,
                [Cloud] TEXT,
                [temperature] TEXT,
                [wind_speed] TEXT,
                [humidity] TEXT,
                [country] TEXT);
                ''')

    # drop existing table
    myDB.delete_table(db_conn, "City_Weather_Data")
    # create weather forecast table
    myDB.create_table(db_conn, create_table_qry)

    # event loop for fetching data from website
    async with aiohttp.ClientSession() as curr_session:
        await periodic_fetch(db_conn, user_api_key, city_name, curr_session)


asyncio.run(main())