import os
import sys

from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "Layout/form.ui"),self)
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)

        self.button1 = self.findChild(QtWidgets.QPushButton, 'play')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pause')
        self.button3 = self.findChild(QtWidgets.QPushButton, 'stop')

        file = os.path.join(os.path.dirname(__file__), "cat.mp4")
        # file="https://www.convertinmp4.com/redirect.php?video=P69pu5Q3ZcQ&v=DXYECd2VK6cJxTZ2o7P2t8TqzGEeP6Sd"
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
        self.player.setVideoOutput(self.ui.widget)
        self.player.play()

        self.button1.clicked.connect(self.player.play) # Remember to pass the definition/method, not the return value!
        self.button2.clicked.connect(self.player.pause) # Remember to pass the definition/method, not the return value!
        self.button3.clicked.connect(self.player.stop) # Remember to pass the definition/method, not the return value!
      
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    w.showFullScreen()
    sys.exit(app.exec())