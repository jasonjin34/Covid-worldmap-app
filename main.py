import sys
import cv2 as cv
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject, pyqtSignal
from readdata import current_data, country_location, gps_coord_trans, edit_map, worldmap, cloest_city
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
        if not self.time:
            return
        virusdatadict = current_data(self.time)
        currloca = (e.x(), e.y())
        closecity = cloest_city(locationdict, currloca)
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
        imgcv = edit_map(temp)
        self.time = temp

        height, width, channel = imgcv.shape
        bytesPerLine = 3 * width
        qImg = QImage(imgcv.data, width, height, bytesPerLine, QImage.Format_BGR888)
        self.maplabel.setPixmap(QPixmap.fromImage(qImg))

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()