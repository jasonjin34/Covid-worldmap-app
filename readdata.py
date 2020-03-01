import csv 
import requests
from datetime import date, timedelta
import math
import cv2
import os

def current_data(time):

    dataurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    dataurl = dataurl + str(time) + '.csv'

    datadict = {}
    totalconfirm, totaldeath, totalrecover = 0, 0, 0    
    with requests.get(dataurl, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        csvreader = csv.reader(lines)
        next(csvreader)
        for row in csvreader:
            country = row[1]
            totalconfirm += int(row[3])
            totaldeath += int(row[4])
            totalrecover += int(row[5])
            if country not in datadict:
                datadict[country] = [int(val) for val in row[3:]]
            else:
                datadict[country] = [val1 + int(val2) for val1, val2 in zip(datadict[country],row[3:])]
    return datadict,totalconfirm, totaldeath, totalrecover

def time_series_data(input):
    timeseriesdataurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'
    timeseriesdataurl = timeseriesdataurl + str(input) + '.csv'
    timeseriedatadict = {}
    with requests.get(timeseriesdataurl, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        csvreader = csv.reader(lines)
        header = next(csvreader)
        #read data
        for row in csvreader:
            country = row[1]
            temptimedata = [int(element) for element in row[4:]]
            if country not in timeseriedatadict:
                timeseriedatadict[country] = temptimedata
            else:
                timeseriedatadict[country] = [val1+val2 for val1, val2 in zip(timeseriedatadict[country], temptimedata)]
    return timeseriedatadict 
    
def country_location():
    geocountrydict = {}
    with open("geocountry.txt", encoding='utf-8') as f:
        f = f.readlines()
        for line in f:
            templist = line.strip().split(',')
            country = str(templist[0]).replace('\'','').strip()
            geo = (float(templist[1]), float(templist[2]))
            geocountrydict[country] = geo
    return geocountrydict

def gps_coord_trans(gps_tuple, R):
    longtitude = gps_tuple[0] / 180.0 * math.pi
    latitude = gps_tuple[1] /180.0 * math.pi
    y = 256.0 - R * longtitude 
    x = 512.0 + R * latitude 
    return x, y

def calc_distance(pos1, pos2):
    deltax = pos1[0] - pos2[0]
    deltay = pos1[1] - pos2[1]
    return math.sqrt(deltax**2 + deltay**2)

def cloest_city(datadict, currloca, time, viruscountry):
    cloest_city = ''
    shortest_distance = 10000
    R = 162.9
    for v, k in datadict.items():
        if v not in viruscountry:
            continue
        temp_x, temp_y = gps_coord_trans(k, R)
        temp_distance = calc_distance(currloca, (temp_x, temp_y)) 
        if temp_distance < shortest_distance:
            shortest_distance = temp_distance 
            cloest_city = v
    if shortest_distance < 200:
        return cloest_city
    else:
        return 
pass
def edit_map(time):
    img = worldmap()
    origin_img = img.copy()
    Radius = 162.9
    locationdata = country_location()
    virusdata,totalconfirm, totaldeath, totalrecover = current_data(time)

    for k, v in virusdata.items():
        country = k
        if not v[0] or country not in locationdata:
            continue
        numberinfect = int(math.log(v[0], 2)) * 2
        latituelongtitue = locationdata[country]
        x_coord, y_coord = gps_coord_trans(latituelongtitue, Radius)
        img = cv2.circle(img, (int(x_coord), int(y_coord)), numberinfect, (0,0,255), -1)

    alpha = 0.4  # Transparency factor.

    # Following line overlays transparent rectangle over the image
    combined_image = cv2.addWeighted(img, alpha, origin_img, 1 - alpha, 0)

    return combined_image, totalconfirm, totaldeath, totalrecover

def worldmap():
    path = './map.png'
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED) 
    return img

if __name__ == "__main__":
    time_series_data()
    