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
import json

with open("config.json", 'r', encoding='utf-8') as jsonFile:
    dados = json.load(jsonFile)

print(dados)

Props = dados['Camera_Properties']['Propriedades']
Filters = dados['Camera_Properties']['Filtros']
Resolutions = dados['Camera_Properties']['resolucao']
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

        self.h_min.setValue(Filters['hmin'])
        self.s_min.setValue(Filters['smin'])
        self.v_min.setValue(Filters['vmin'])
        self.h_max.setValue(Filters['hmax'])
        self.s_max.setValue(Filters['smax'])
        self.v_max.setValue(Filters['vmax'])

        self.brilho.setValue(Props['brilho'])
        self.matiz.setValue(Props['matiz'])
        self.gama.setValue(Props['gama'])
        self.saturacao.setValue(Props['saturacao'])
        self.contrast.setValue(Props['contrast'])
        self.ganho.setValue(Props['ganho'])
        self.luzfundo.setValue(Props['luzfundo'])
        self.exposicao.setValue(Props['exposicao'])

        self.SHOW.clicked.connect(self.onClicked)
        self.change.clicked.connect(self.Troca)
        self.TEXT.setText("Aperte Start para exibir a imagem")
        self.CAPTURE.clicked.connect(self.CaptureClicked)

    @pyqtSlot()
    def Troca(self):
        if self.logic == 0:
            self.logic = 3
            self.change.setText('Verificar')
        elif self.logic == 3:
            self.logic = 4
            self.change.setText('Detectar')
        elif self.logic == 4:
            self.change.setText('Medir')
            self.logic = 0

    def MascaraHSV(self, img, **kwargs):
        if kwargs.get('lower') and kwargs.get('upper'):
            mask = cv2.morphologyEx(cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), np.array(kwargs.get('lower')),
                                                np.array(kwargs.get('upper'))), cv2.MORPH_OPEN,
                                    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

        else:
            mask = cv2.morphologyEx(cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV),
                                                np.array(
                                                    [kwargs.get('h_min'), kwargs.get('s_min'), kwargs.get('v_min')]),
                                                np.array(
                                                    [kwargs.get('h_max'), kwargs.get('s_max'), kwargs.get('v_max')])),
                                    cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        if kwargs.get('mask'):
            return mask
        else:
            return cv2.bitwise_and(img, img, mask=mask)

    def Atualiza(self, cap):

        cap.set(cv2.CAP_PROP_BRIGHTNESS, self.brilho.value())
        cap.set(cv2.CAP_PROP_HUE, self.matiz.value())
        cap.set(cv2.CAP_PROP_CONTRAST, self.contrast.value())
        cap.set(cv2.CAP_PROP_GAMMA, self.gama.value())
        cap.set(cv2.CAP_PROP_GAIN, self.ganho.value())
        cap.set(cv2.CAP_PROP_SATURATION, self.saturacao.value())
        cap.set(cv2.CAP_PROP_BACKLIGHT, self.luzfundo.value())
        cap.set(cv2.CAP_PROP_EXPOSURE, self.exposicao.value())

    # def Mascara(self, img):
    #     imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     if self.logic == 0:
    #         lower = np.array([self.h_min.value(), self.s_min.value(), self.v_min.value()], np.uint8)
    #         upper = np.array([self.h_max.value(), self.s_max.value(), self.v_max.value()], np.uint8)
    #         self.d_old_h_min = lower[0]
    #         self.d_old_s_min = lower[1]
    #         self.d_old_v_min = lower[2]
    #         self.d_old_h_max = upper[0]
    #         self.d_old_s_max = upper[1]
    #         self.d_old_v_max = upper[2]
    #         mask = cv2.inRange(imgHsv, lower, upper)
    #         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    #         return mask
    #     elif self.logic == 3:
    #         lower = np.array([self.h_min.value(), self.s_min.value(), self.v_min.value()], np.uint8)
    #         upper = np.array([self.h_max.value(), self.s_max.value(), self.v_max.value()], np.uint8)
    #         self.m_old_h_min = lower[0]
    #         self.m_old_s_min = lower[1]
    #         self.m_old_v_min = lower[2]
    #         self.m_old_h_max = upper[0]
    #         self.m_old_s_max = upper[1]
    #         self.m_old_v_max = upper[2]
    #         mask = cv2.inRange(imgHsv, lower, upper)
    #         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    #         return mask
    def onClicked(self):
        cap = cv2.VideoCapture(0)
        # address = "rtsp://admin:admin@192.168.25.10/cam/realmonitor?channel=1&subtype=0"
        # cap.open(address)
        # ret, imgcopy = cap.read()
        while cap.isOpened():
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # h, w = img.shape[:2]
            # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            # img = cv2.undistort(img, mtx, dist, None, newcameramtx)
            self.Atualiza(cap)
            if self.logic == 0:
                self.displayImage(img, 1)
                cv2.waitKey(2)
            elif self.logic == 3:

                self.displayImage(self.MascaraHSV(img, lower=[self.h_min.value(),
                                                              self.s_min.value(),
                                                              self.v_min.value(),
                                                              ],
                                                  upper=[
                                                      self.h_max.value(),
                                                      self.s_max.value(),
                                                      self.v_max.value()]), 1)
                cv2.waitKey(2)
            elif self.logic == 4:
                self.displayImage(HSV, 1)
                cv2.waitKey(2)
            if self.logic == 2:
                dados['Camera_Properties']['Propriedades'] = {
                    "brilho": self.brilho.value(),
                    "matiz": self.matiz.value(),
                    "contrast": self.contrast.value(),
                    "gama": self.gama.value(),
                    "ganho": self.ganho.value(),
                    "saturacao": self.saturacao.value(),
                    "luzfundo": self.luzfundo.value(),
                    "exposicao": self.exposicao.value()
                }
                dados['Camera_Properties']['Filtros']['hmin'] = self.h_min.value()
                dados['Camera_Properties']['Filtros']['smin'] = self.s_min.value()
                dados['Camera_Properties']['Filtros']['vmin'] = self.v_min.value()
                dados['Camera_Properties']['Filtros']['hmax'] = self.h_max.value()
                dados['Camera_Properties']['Filtros']['smax'] = self.s_max.value()
                dados['Camera_Properties']['Filtros']['vmax'] = self.v_max.value()
                with open("config.json", 'w', encoding='utf-8') as jsonFile2:
                    json.dump(dados, jsonFile2, indent=4)
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()

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
