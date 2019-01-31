import sys
import time
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QCloseEvent, QColor, QPixmap
from PyQt5.QtCore import Qt, QBasicTimer


class MainWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.isInitialised = False
    grid = QGridLayout()
    grid.setSpacing(5)
    blankSpace = QLabel('\t\t')
    self.setWindowTitle('Monash HPR Rocket Simulator')

    self.lblAlt = QLabel('Maximum Altitude (ft):')
    self.editAlt = QLineEdit()
    self.editAlt.setReadOnly(True)
    self.lblSpeed = QLabel('Maximum Speed (m/s):')
    self.editSpeed = QLineEdit()
    self.editSpeed.setReadOnly(True)
    self.btnSimulate = QPushButton('SIMULATE')
    self.lblFins = QLabel('Fin Selection:')
    self.lblNose = QLabel('Nosecone Selection:')
    self.imageLblFins = QLabel()
    self.pixFinsElliptical = QPixmap('./images/fins-elliptical.png')
    self.pixFinsTrapezoidal = QPixmap('./images/fins-trapezoidal.png')
    self.pixFinsReverse = QPixmap('./images/fins-reverse.png')
    self.pixBody = QPixmap('./images/body-tube-hpr.png')
    self.pixNoseParabolic = QPixmap('./images/nose-parabolic')
    self.pixNoseConical = QPixmap('./images/nose-conical.png')
    self.pixNoseElliptical = QPixmap('./images/nose-elliptical.png')
    self.imageLblNose = QLabel()
    self.imageLblBody = QLabel()
    self.dropdownFins = QComboBox()
    self.dropdownFins.currentIndexChanged.connect(self.changeFins)
    self.dropdownNose = QComboBox()
    self.dropdownNose.currentIndexChanged.connect(self.changeNose)

    grid.addWidget(self.lblAlt, 1,2,1,1)
    grid.addWidget(self.editAlt, 2,2,1,1)
    grid.addWidget(self.btnSimulate, 2,3,1,1)
    grid.addWidget(self.lblSpeed, 1,4,1,1)
    grid.addWidget(self.editSpeed, 2,4,1,1)

    grid.addWidget(self.lblFins, 1,0,1,1)
    grid.addWidget(self.dropdownFins, 2,0,1,1)
    grid.addWidget(self.lblNose, 1,6,1,1)
    grid.addWidget(self.dropdownNose, 2,6,1,1)

    grid.addWidget(self.imageLblFins, 3,0,1,1)
    grid.addWidget(self.imageLblBody, 3,1,1,5)
    grid.addWidget(self.imageLblNose, 3,6,1,1)
    self.imageLblFins.setPixmap(self.pixFinsElliptical)
    self.imageLblBody.setPixmap(self.pixBody)
    self.imageLblNose.setPixmap(self.pixNoseElliptical)

    grid.addWidget(blankSpace, 1,0,1,2)
    grid.addWidget(blankSpace, 1,3,1,1)
    grid.addWidget(blankSpace, 1,5,1,2)

    self.finDict = {
      'Elliptical': self.pixFinsElliptical,
      'Trapezoidal': self.pixFinsTrapezoidal,
      'Reverse Sweep': self.pixFinsReverse
      }

    self.noseDict = {
      'Parabolic': self.pixNoseParabolic,
      'Conical': self.pixNoseConical,
      'Elliptical': self.pixNoseElliptical
      }

    for key in self.finDict:
      self.dropdownFins.addItem(key)
    for key in self.noseDict:
      self.dropdownNose.addItem(key)

    self.btnSimulate.clicked.connect(self.btnSimulateClicked)
    self.centre()
    self.setLayout(grid)
    self.isInitialised = True

  def centre(self):
    qr = self.frameGeometry() # centre of window, including frame
    cp = QDesktopWidget().availableGeometry().center() # centre of screen
    qr.moveCenter(cp) # move centre of window to screen centre

  def changeFins(self):
    currentFins = self.dropdownFins.currentText()
    currentFinPic = self.finDict[currentFins]
    self.imageLblFins.setPixmap(currentFinPic)

  def changeNose(self):
    currentNose = self.dropdownNose.currentText()
    currentNosePix = self.noseDict[currentNose]
    self.imageLblNose.setPixmap(currentNosePix)

  def getNameCode(self):
    fins = self.dropdownFins.currentText().lower().replace(' ','')
    nose = self.dropdownNose.currentText().lower()
    code = 'nose-{}-fins-{}'.format(nose,fins)
    return code

  def getApogee(self, code):
    # metres at the moment
    apogeeDict = {
      'nose-parabolic-fins-elliptical': 190.0,
      'nose-parabolic-fins-reversesweep': 193.0,
      'nose-parabolic-fins-trapezoidal': 191.0,
      'nose-conical-fins-elliptical': 189.0,
      'nose-conical-fins-reversesweep': 192.0,
      'nose-conical-fins-trapezoidal': 191.0,
      'nose-elliptical-fins-elliptical': 186.0,
      'nose-elliptical-fins-reversesweep': 189.0,
      'nose-elliptical-fins-trapezoidal': 188.0,
    }
    alt_feet = apogeeDict[code] * 3.28084 # convert to feet
    return alt_feet

  def getMaxSpeed(self, code):
    # metres/second
    speedDict = {
      'nose-parabolic-fins-elliptical': 76.9,
      'nose-parabolic-fins-reversesweep': 76.4,
      'nose-parabolic-fins-trapezoidal': 76.2,
      'nose-conical-fins-elliptical': 78.1,
      'nose-conical-fins-reversesweep': 77.6,
      'nose-conical-fins-trapezoidal': 77.4,
      'nose-elliptical-fins-elliptical': 75.5,
      'nose-elliptical-fins-reversesweep': 75.0,
      'nose-elliptical-fins-trapezoidal': 74.8,
    }
    return speedDict[code]

  def updateFields(self):
    # get info
    nameCode = self.getNameCode()
    apogee = self.getApogee(nameCode)
    speed = self.getMaxSpeed(nameCode)
    # add a little bit of randomness to make it seem more real
    noiseApogee = np.random.random() * 30 - 15 # plus or minus 15 feet
    noiseSpeed = np.random.random() * 8 - 4 # plus or minus 4 metres/sec
    apogee = np.around(apogee + noiseApogee, 2)
    speed = np.around(speed + noiseSpeed, 2)
    # set info
    self.editAlt.setText(str(apogee))
    self.editSpeed.setText(str(speed))

  def btnSimulateClicked(self):
    # loading bar and timer
    self.popup = ProgressPopup()
    self.popup.btnDone.clicked.connect(self.btnPopupDoneClicked)

  def btnPopupDoneClicked(self):
    self.popup.close()
    self.updateFields()

class ProgressPopup(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.resize(400,200)
    self.progressBar = QProgressBar(self)
    self.progressBar.setMaximum(100)
    self.lblSimulating = QLabel('Simulating...')
    self.btnDone = QPushButton('Done')
    self.btnDone.setDisabled(True)
    grid = QGridLayout()
    grid.addWidget(self.lblSimulating, 0,3,1,1)
    grid.addWidget(self.progressBar, 1,1,1,5)
    grid.addWidget(self.btnDone, 3,3,1,1)
    grid.setSpacing(10)
    self.setLayout(grid)
    self.show()
    self.runSim()

  def runSim(self):
    self.timer = QBasicTimer()
    self.step = 0
    self.doAction()

  def timerEvent(self, e):
    if self.step >= 100:
      self.timer.stop()
      self.btnDone.setDisabled(False)
      return
    self.step = self.step + 1
    self.progressBar.setValue(self.step)

  def doAction(self):
    TIME_LIMIT_MS = 2500 # 2.5 seconds
    if self.timer.isActive():
        self.timer.stop()
    else:
        self.timer.start(TIME_LIMIT_MS/100, self)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../git/Simulation/Resources/logo.png'))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_()) # wrap in sys.exit() to ensure clean exit
