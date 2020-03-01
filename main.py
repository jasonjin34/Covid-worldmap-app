import sys
import cv2 as cv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets, uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QObject, pyqtSignal
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 

from readdata import current_data, country_location, gps_coord_trans, edit_map, worldmap, cloest_city, time_series_data

from MainWindow import Ui_MainWindow
from Dialog import Ui_Dialog

class message(QObject):
    message = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.value = ()


class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('Detail Convid-19')
        self.scene = pg.PlotWidget()        
        self.plotbotton.pressed.connect(self.plot_series_data)
    
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
        #read the time serise data 
        location = self.location
        timeseriesdictconfirmed = time_series_data('Confirmed')
        timeseriesdictdeaths = time_series_data('Deaths')
        timeseriesdictrecover = time_series_data('Recovered')

        timedataconfirmed = timeseriesdictconfirmed[location]
        timedatadeaths = timeseriesdictdeaths[location]
        timedatarecover = timeseriesdictrecover[location]
        length = len(timedataconfirmed)
        data = [x for x in range(length)] 


        self.scene.setBackground('w')
        self.scene.setTitle("Covid-19")
        self.scene.setLabel('left', 'Confirmed Cases', color=(0,0,0), size=10)
        self.scene.setLabel('bottom', 'date', color=(0,0,0), size=10)
        self.scene.addLegend()
        self.scene.showGrid(x=False, y=True)

        pen1 = pg.mkPen(color=(255, 165, 000), width=2)
        pen2 = pg.mkPen(color=(000, 000, 000), width=2)
        pen3 = pg.mkPen(color=(50, 205, 50), width=2)

        self.scene.plot(data, timedataconfirmed, name='Confirmed', pen=pen1, symbol='o', symbolSize=4)
        self.scene.plot(data, timedatadeaths, name='Death', pen=pen2, symbol='x', symbolSize=4)
        self.scene.plot(data, timedatarecover, name='Recover', pen=pen3, symbol='+', symbolSize=4)
        self.scene.show()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.time = None
        #set mouse traning
        self.setMouseTracking(True)
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

    def mousePressEvent(self, e):
        #get country location
        locationdict = country_location()
        virusdatadict, _, _, _= current_data(self.time)
        currloca = (e.x(), e.y())
        closecity = cloest_city(locationdict, currloca, self.time, virusdatadict)
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