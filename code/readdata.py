import csv 
import requests
from datetime import date, timedelta
import math
import cv2
import os
import matplotlib.pyplot as plt

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
            row = [e if e else '0' for e in row]
            if not row:
                return
            country = row[1]
            totalconfirm += int(row[3])
            totaldeath += int(row[4])
            totalrecover += int(row[5])
            if country not in datadict:
                datadict[country] = [int(val) for val in row[3:6]]
            else:
                datadict[country] = [val1 + int(val2) for val1, val2 in zip(datadict[country],row[3:6])]
    return datadict,totalconfirm, totaldeath, totalrecover

def date_data_for_checkbox():
    timeseriesdataurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    r = requests.get(timeseriesdataurl, stream=True)
    r = (line.decode('utf-8') for line in r.iter_lines())
    header = next(csv.reader(r))
    output = []
    for data in header[4:]:
        templist = data.split('/')
        month = templist[0]
        if len(month) == 1:
            month = '0' + month
        day = templist[1]
        if len(day) == 1:
            day = '0' + day
        year = templist[2] + '20'
        output.append('{}-{}-{}'.format(month, day, year))
    return output

def time_series_data(input):
    timeseriesdataurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'
    timeseriesdataurl = timeseriesdataurl + str(input) + '.csv'
    timeseriedatadict = {}
    with requests.get(timeseriesdataurl, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())
        csvreader = csv.reader(lines)
        header = next(csvreader)
        header = [date[:-3] for date in header[4:]]
        #read data
        for row in csvreader:
            if not row:
                continue
            country = row[1]
            temptimedata = [int(element) if element else 0 for element in row[4:]]
            if country not in timeseriedatadict:
                timeseriedatadict[country] = temptimedata
            else:
                timeseriedatadict[country] = [val1+val2 for val1, val2 in zip(timeseriedatadict[country], temptimedata)]
    return timeseriedatadict, header 
    
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

def gps_coord_reverse_trans(x, y):
    longtitude = - (y - 256) / 162.9
    latitude = (x - 512) / 162.9
    longtitude = longtitude / math.pi * 180.0
    latitude = latitude / math.pi * 180.0
    return longtitude, latitude

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
    if shortest_distance < 50:
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
    print(time)

    for k, v in virusdata.items():
        country = k
        if not v[0] or country not in locationdata:
            continue
        radius = int(math.log2(v[0])) * 2
        latituelongtitue = locationdata[country]
        x_coord, y_coord = gps_coord_trans(latituelongtitue, Radius)

        if v[0] >= 10000:
            color = 0
        elif v[0] < 10000 and v[0] > 1000:
            color = 80
        elif v[0] < 1000 and v[0] > 100:
            color = 160
        elif v[0] < 100:
            color = 255
        
        img = cv2.circle(img, (int(x_coord), int(y_coord)), radius, (0,0,color), -1)

    alpha = 0.4  # Transparency factor.

    # Following line overlays transparent rectangle over the image
    combined_image = cv2.addWeighted(img, alpha, origin_img, 1 - alpha, 0)

    return combined_image, totalconfirm, totaldeath, totalrecover

def worldmap():
    path = './map.png'
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED) 
    return img

def plottimeserisedata():
    plt.figure(figsize=(20,10))
    confirmdata, header= time_series_data('Confirmed')
    korea = confirmdata['South Korea']
    italy = confirmdata['Italy']
    germany = confirmdata['Germany']
    spain = confirmdata['Spain']
    france = confirmdata['France']
    
    #slope
    koreabefore = korea[-17:-1]
    koreaafter = korea[-16:]
    italybefore = italy[-17:-1]
    italyafter = italy[-16:]
    spainbefore = spain[-17:-1]
    spainafter = spain[-16:]
    francebefore = france[-17:-1]
    franceafter = france[-16:]
    germanybefore = germany[-17:-1]
    spainafter = spain[-16:]
    germanybefore = germany[-17:-1]
    germanyafter = germany[-16:]

    slopkorea = [after - before for after, before in zip(koreaafter, koreabefore)]
    slopitaly = [after - before for after, before in zip(italyafter, italybefore)]
    slopgermany = [after - before for after, before in zip(germanyafter, germanybefore)]
    slopspain = [after - before for after, before in zip(spainafter, spainbefore)]
    slopfrance = [after - before for after, before in zip(franceafter, francebefore)]
    slopheader = header[-16:]

    ax1 = plt.subplot(121)
    ax1.plot(slopheader, slopkorea, label='Korea Growth Rate')
    ax1.plot(slopheader, slopitaly, label='Italy Growth Rate')
    ax1.plot(slopheader, slopgermany, label='Germany Growth Rate')
    ax1.plot(slopheader, slopspain, label='Spain Growth Rate')
    ax1.plot(slopheader, slopfrance, label='France Growth Rate')
    plt.legend()
    plt.yscale('log')
    plt.grid()
    ax1.title.set_text("Growth Slope")
    
    ax2=plt.subplot(122)
    ax2.plot(header[-17:], korea[-17:], label='Korea')
    ax2.plot(header[-17:], italy[-17:], label='Italy')
    ax2.plot(header[-17:], germany[-17:], label='Germany')
    ax2.plot(header[-17:], spain[-17:], label='Spain')
    ax2.plot(header[-17:], france[-17:], label='France')
    ax2.title.set_text("Number of Confirmed Case")
    plt.legend()
    plt.grid()
    plt.yscale('log')

    plt.show()

if __name__ == "__main__":
    plottimeserisedata()
    