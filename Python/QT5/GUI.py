import sys
import numpy as np
import pickle

import cv2
import imutils
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

#dist_pickle = pickle.load(open("camera_cal.p", "rb"))
#dist = dist_pickle["dist"]
#mtx = dist_pickle["mtx"]
#config = pickle.load(open("arquivo.p", "rb"))

Neighbors = 0  # config["Neighbors"]
AreaMax = 0  # config["AreaMax"]
Scale = 0  # config["Scale"]

mhmin = 0  # config["mhmin"]
msmin = 0  # config["msmin"]
mvmin = 0  # config["mvmin"]

mhmax = 255  # config["mhmax"]
msmax = 255  # config["msmax"]
mvmax = 255  # config["mvmax"]

dhmin = 0  # config["dhmin"]
dsmin = 0  # config["dsmin"]
dvmin = 0  # config["dvmin"]

dhmax = 255  # config["dhmax"]
dsmax = 255  # config["dsmax"]
dvmax = 255  # config["dvmax"]


class tehseencode(QDialog):

    def __init__(self):
        super(tehseencode, self).__init__()
        loadUi("graph.ui", self)

        self.logic = 0
        self.value = 1

        self.neg.setValue(Neighbors)
        self.scle.setValue(Scale)
        self.MaxPx.setValue(AreaMax)

        self.h_min.setValue(dhmin)
        self.s_min.setValue(dsmin)
        self.v_min.setValue(dvmin)
        self.h_max.setValue(dhmax)
        self.s_max.setValue(dsmax)
        self.v_max.setValue(dvmax)

        self.m_old_h_min = mhmin
        self.m_old_s_min = msmin
        self.m_old_v_min = mvmin
        self.m_old_h_max = mhmax
        self.m_old_s_max = msmax
        self.m_old_v_max = mvmax

        self.SHOW.clicked.connect(self.onClicked)
        self.change.clicked.connect(self.Troca)
        self.TEXT.setText("Aperte Start para exibir a imagem")
        self.CAPTURE.clicked.connect(self.CaptureClicked)

    @pyqtSlot()
    def Troca(self):
        if self.logic == 0:
            self.logic = 3
            # self.h_min.setValue(self.m_old_h_min)
            # self.s_min.setValue(self.m_old_s_min)
            # self.v_min.setValue(self.m_old_v_min)
            # self.h_max.setValue(self.m_old_h_max)
            # self.s_max.setValue(self.m_old_s_max)
            # self.v_max.setValue(self.m_old_v_max)
            self.change.setText('Verificar')
        elif self.logic == 3:
            self.logic = 4
            # self.h_min.setValue(self.d_old_h_min)
            # self.s_min.setValue(self.d_old_s_min)
            # self.v_min.setValue(self.d_old_v_min)
            # self.h_max.setValue(self.d_old_h_max)
            # self.s_max.setValue(self.d_old_s_max)
            # self.v_max.setValue(self.d_old_v_max)
            self.change.setText('Detectar')
        elif self.logic == 4:
            self.change.setText('Medir')
            self.logic = 0

    def Mascara(self, img):
        imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if self.logic == 0:
            lower = np.array([self.h_min.value(), self.s_min.value(), self.v_min.value()], np.uint8)
            upper = np.array([self.h_max.value(), self.s_max.value(), self.v_max.value()], np.uint8)
            self.d_old_h_min = lower[0]
            self.d_old_s_min = lower[1]
            self.d_old_v_min = lower[2]
            self.d_old_h_max = upper[0]
            self.d_old_s_max = upper[1]
            self.d_old_v_max = upper[2]
            mask = cv2.inRange(imgHsv, lower, upper)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
            return mask
        elif self.logic == 3:
            lower = np.array([self.h_min.value(), self.s_min.value(), self.v_min.value()], np.uint8)
            upper = np.array([self.h_max.value(), self.s_max.value(), self.v_max.value()], np.uint8)
            self.m_old_h_min = lower[0]
            self.m_old_s_min = lower[1]
            self.m_old_v_min = lower[2]
            self.m_old_h_max = upper[0]
            self.m_old_s_max = upper[1]
            self.m_old_v_max = upper[2]
            mask = cv2.inRange(imgHsv, lower, upper)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
            return mask

    def onClicked(self):
        cap = cv2.VideoCapture(0)
        # address = "rtsp://admin:admin@192.168.25.10/cam/realmonitor?channel=1&subtype=0"
        # cap.open(address)
        # ret, imgcopy = cap.read()
        while cap.isOpened():
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            HSV = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # h, w = img.shape[:2]
            # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            # img = cv2.undistort(img, mtx, dist, None, newcameramtx)
            if self.logic == 0:
                self.displayImage(img, 1)
                print("Zerin")
                cv2.waitKey(2)
            elif self.logic == 3:
                print("Treixxx")
                self.displayImage(gray, 1)
                cv2.waitKey(2)
            elif self.logic == 4:
                print("Quatro")
                self.displayImage(HSV, 1)
                cv2.waitKey(2)
            if self.logic == 2:
                print("Dois")
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()
        cv2.destroyAllWindows()
        cap.release()

    def CaptureClicked(self):
        cv2.destroyAllWindows()
        self.logic = 2

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


app = QApplication(sys.argv)
window = tehseencode()
window.show()
sys.exit(app.exec_())
