import sys
import cv2 as cv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets, uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QObject, pyqtSignal
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 

from readdata import current_data, country_location, gps_coord_trans, edit_map, worldmap, cloest_city, time_series_data, gps_coord_reverse_trans

from MainWindow import Ui_MainWindow
from Dialog import Ui_Dialog


class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('Detail Convid-19')

        #signal slot connection
        self.plotbotton.pressed.connect(self.plot_series_data)
        self.recovercheckBox.stateChanged.connect(self.plot_series_data)
        self.deathcheckBox.stateChanged.connect(self.plot_series_data)

        #set up for ploting
        self.plotwidget.setBackground('w')
        self.plotwidget.setTitle("Covid-19")
        self.plotwidget.setLabel('left', 'Confirmed Cases', color=(0,0,0), size=10)
        self.plotwidget.setLabel('bottom', 'past date', color=(0,0,0), size=10)
        self.plotwidget.showGrid(x=False, y=True)

        #set up pen
        self.pen1 = pg.mkPen(color=(255, 165, 000), width=2)
        self.pen2 = pg.mkPen(color=(000, 000, 000), width=2)
        self.pen3 = pg.mkPen(color=(50, 205, 50), width=2)
        
        #set up lengend
        self.plotwidget.addLegend()
        style = pg.PlotDataItem(pen=self.pen1)
        self.plotwidget.plotItem.legend.addItem(style, 'Confirm')
        style = pg.PlotDataItem(pen=self.pen2)
        self.plotwidget.plotItem.legend.addItem(style, 'Deaths')
        style = pg.PlotDataItem(pen=self.pen3)
        self.plotwidget.plotItem.legend.addItem(style, 'Reovered')

        self.xax = self.plotwidget.getAxis('bottom')

        self.xax = self.plotwidget.getAxis('bottom')
        #read the time serise data 
        self.timeseriesdictconfirmed, self.dateheader = time_series_data('Confirmed')
        self.timeseriesdictdeaths, _ = time_series_data('Deaths')
        self.timeseriesdictrecover, _ = time_series_data('Recovered')
        length = len(self.dateheader)
        self.data = [x for x in range(length)]
        ticket = [list(zip(self.data[::4], self.dateheader[::4]))]
        self.xax.setTicks(ticket)

   
    def setData(self, location, data):
        #get the city number of confirmed, death and recover cases 
        self.countrylineEdit.setText(location)
        self.countrylineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        data = [str(temp) for temp in data]
        self.ConfiredlineEdit.setText(data[0])
        self.ConfiredlineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.DeathslineEdit.setText(data[1])
        self.DeathslineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.RecoveredlineEdit.setText(data[2])
        self.RecoveredlineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.location = location
    
    def plot_series_data(self):
        self.plotwidget.clear()

        data = self.data
        location = self.location

        #plot cases difference
        recoverstate, deathstate = self.recovercheckBox.isChecked(), self.deathcheckBox.isChecked() 
        if not recoverstate and not deathstate:
            timedataconfirmed = self.timeseriesdictconfirmed[location]
            self.plotwidget.plot(data, timedataconfirmed, pen=self.pen1, symbol='o', symbolSize=4)
            timedatadeaths = self.timeseriesdictdeaths[location]
            self.plotwidget.plot(data, timedatadeaths, pen=self.pen2, symbol='x', symbolSize=4)
            timedatarecover = self.timeseriesdictrecover[location]
            self.plotwidget.plot(data, timedatarecover, pen=self.pen3, symbol='+', symbolSize=4)        

        if deathstate:
            timedatadeaths = self.timeseriesdictdeaths[location]
            self.plotwidget.plot(data, timedatadeaths, pen=self.pen2, symbol='x', symbolSize=4)
            
        if recoverstate: 
            timedatarecover = self.timeseriesdictrecover[location]
            self.plotwidget.plot(data, timedatarecover, pen=self.pen3, symbol='+', symbolSize=4)        

        self.plotwidget.show()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.time = None
        self.setWindowTitle("Coronavirus map: how Covid-19 is spreading across the world")

        #set up the origin image
        imgcv = worldmap()
        height, width, channel = imgcv.shape
        bytesPerLine = 3 * width
        qImg = QImage(imgcv.data, width, height, bytesPerLine, QImage.Format_BGR888)
        self.maplabel.setPixmap(QPixmap.fromImage(qImg))

        #set dateEdit 
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.dateChanged.connect(self.refresh)

        #reload data
        self.locationdict = country_location()

        #tracking mouse in map label
        self.maplabel.setMouseTracking(True)
    
    def mouseMoveEvent(self, e):
        #get country location
        virusdatadict, _, _, _= current_data(self.time)
        currloca = (e.x() - 10, e.y() - 10)
        closecity = cloest_city(self.locationdict, currloca, self.time, virusdatadict)
        if not closecity:
            self.mouseCountry.setText('Country') 
            return
        #QDialog of detail Virus information
        dlg = Dialog()
        #get the city data
        if closecity not in virusdatadict:
            self.mouseCountry.setText('Country')
            return
        self.mouseCountry.setText(closecity)


    def mousePressEvent(self, e):
        #get country location
        virusdatadict, _, _, _= current_data(self.time)
        currloca = (e.x() - 10, e.y() - 10)
        closecity = cloest_city(self.locationdict, currloca, self.time, virusdatadict)
        if not closecity:
            return
        #QDialog of detail Virus information
        dlg = Dialog()
        #get the city data
        if closecity not in virusdatadict:
            return
        citydata = virusdatadict[closecity]
        dlg.setData(closecity, citydata)
        dlg.exec_()        
        log, lat = gps_coord_reverse_trans(e.x(), e.y()) 
        print('longtitue: {}, latitute: {}'.format(log, lat))

    def refresh(self):
        temp = self.dateEdit.date().toString("MM-dd-yyyy")
        if temp == '02-10-2020':
            return
        imgcv, totalconfirm, totaldeath, totalrecover = edit_map(temp)
        self.time = temp
        height, width, channel = imgcv.shape
        bytesPerLine = 3 * width
        qImg = QImage(imgcv.data, width, height, bytesPerLine, QImage.Format_BGR888)
        self.maplabel.setPixmap(QPixmap.fromImage(qImg))

        #get the total data
        self.confirmLineEdit.setText(str(totalconfirm))
        self.deathLineEdit.setText(str(totaldeath))
        self.recoverLineEdit.setText(str(totalrecover))

        self.confirmLineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.deathLineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.recoverLineEdit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()