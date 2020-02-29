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
    with requests.get(dataurl, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        csvreader = csv.reader(lines)
        next(csvreader)
        for row in csvreader:
            country = row[1]
            if country not in datadict:
                datadict[country] = [int(val) for val in row[3:]]
            else:
                datadict[country] = [val1 + int(val2) for val1, val2 in zip(datadict[country],row[3:])]
    return datadict

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
    return int(x), int(y)

def calc_distance(pos1, pos2):
    deltax = pos1[0] - pos2[0]
    deltay = pos1[1] - pos2[1]
    return math.sqrt(deltax**2 + deltay**2)

def cloest_city(datadict, currloca):
    time = date.today() - timedelta(days=1)
    time = time.strftime("%m-%d-%Y")
    viruscountry = current_data(time)
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
    return cloest_city
        

def edit_map(time):
    img = worldmap()
    origin_img = img.copy()
    Radius = 162.9
    locationdata = country_location()
    virusdata = current_data(time)

    for k, v in virusdata.items():
        country = k
        if not v[0] or country not in locationdata:
            continue
        numberinfect = int((math.log10(v[0]))**2 + 5)
        latituelongtitue = locationdata[country]
        x_coord, y_coord = gps_coord_trans(latituelongtitue, Radius)
        img = cv2.circle(img, (x_coord, y_coord), numberinfect, (0,0,255), -1)

    alpha = 0.4  # Transparency factor.

    # Following line overlays transparent rectangle over the image
    combined_image = cv2.addWeighted(img, alpha, origin_img, 1 - alpha, 0)

    return combined_image

def worldmap():
    path = './map.png'
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED) 
    return img



