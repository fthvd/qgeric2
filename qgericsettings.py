# -*- coding: utf-8 -*-

# Qgeric: plugin that makes selecting easier
# Author: Jérémy Kalsron
#         jeremy.kalsron@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from builtins import str

from qgis.PyQt.QtWidgets import QWidget, QPushButton, QCheckBox, QSlider, QDesktopWidget,\
    QLabel, QColorDialog, QVBoxLayout, QFontDialog, QMessageBox

from qgis.PyQt.QtGui import QColor, QFont

from qgis.PyQt.QtCore import Qt, QCoreApplication, pyqtSignal, QVariant

from qgis.core import QgsSettings, QgsProject, QgsVectorLayer, QgsVectorFileWriter,\
    QgsWkbTypes, QgsField, QgsFields, QgsLayerTree, QgsApplication

from qgis.utils import iface

import os, unicodedata

from . import resources

class QgericSettings(QWidget):
    """Window used to change settings (transparency/color/event layers/layers path)"""
    settingsChanged = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle(self.tr('Qgeric - Settings'))
        # self.setFixedSize(400, 180)
        self.center()
        self.keepselect = False

        self.chkbox_selectedlayers = QCheckBox(self.tr('Keep selection in layer manager'), self)
        self.chkbox_selectedlayers.clicked.connect(self.handler_selectedLayers)

        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl_opacity)
        # vbox.addWidget(self.sld_opacity)
        # vbox.addWidget(self.btn_chColor)
        # vbox.addWidget(self.btn_chFont)
        # vbox.addWidget(self.btn_chColorFont)
        vbox.addWidget(self.chkbox_selectedlayers)
        self.setLayout(vbox)

    def tr(self, message):
        return QCoreApplication.translate('Qgeric', message)

    def handler_selectedLayers(self):
        self.iface = iface
        if self.chkbox_selectedlayers.checkState():
            msg = self.tr("The display of the selections will be preserved.")
            self.keepselect = True
        else:
            msg = self.tr("The display of selections will be removed.")
            self.keepselect = False
            # Suppression d'une éventuelle sélection en cours
            root = QgsProject.instance().layerTreeRoot()
            for checked_layers in root.checkedLayers():
                try:
                    checked_layers.removeSelection()
                except:
                    pass
        QMessageBox.information(
            self.iface.mainWindow(),
            self.tr("Fenêtre carte : "), msg)
        self.close()
        # return keepselect

    def handler_convertEventLayers(self):
        self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def showEvent(self, o):
        # print('show passé')
        # self.verifEVT()
        o.accept()

    def closeEvent(self, e):
        self.clear()
        e.accept()

    def clear(self):
        return

