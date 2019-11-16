import os
import sys
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore
import mysql.connector
import register
import dashboard
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="Edudroid"
)


class loginClass(QtWidgets.QDialog):
    
    switch_next_window=QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "Layout/login_new.ui"),self)

        self.button1 = self.findChild(QtWidgets.QPushButton, 'register_2')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'login')
        self.button3 = self.findChild(QtWidgets.QPushButton, 'guest')

        self.email = self.findChild(QtWidgets.QLineEdit, 'email')
        self.passwd = self.findChild(QtWidgets.QLineEdit, 'passwd')

        self.button1.clicked.connect(self.register)
        self.button2.clicked.connect(self.loginFun)
        self.button3.clicked.connect(self.guestFun)

    def register(self):
        print("register")
        register.RegisterClass.startWin(self)
        self.close()

    def loginFun(self):
        useremail=self.email.text()
        userpasswd=self.passwd.text()
        query='select * from Student where student_email = "'+useremail+'" and student_password = "'+userpasswd+'"'
        
        my_database = db_connection.cursor()
        
        my_database.execute(query)
        output = my_database.fetchall()
        
        if my_database.rowcount>0:
            print("logged in")
            self.close()
            dashboard.dashboard.startWin(self)
        else:
            print("incorrect password")


    def guestFun(self):
        print("guest")
        dashboard.dashboard.startWin(self)
        self.hide()

    def startWin(self):
        window = loginClass(self)
        window.showFullScreen()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = loginClass()
    w.showFullScreen()
    sys.exit(app.exec())