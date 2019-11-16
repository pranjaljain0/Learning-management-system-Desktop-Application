import os
import sys
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore
import mysql.connector
import login1
import dashboard

db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="Edudroid"
)

class RegisterClass(QtWidgets.QDialog):
      
    switch_next_window=QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "Layout/register.ui"),self)
        # self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)

        self.button1 = self.findChild(QtWidgets.QPushButton, 'register_2')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'login')
        self.button3 = self.findChild(QtWidgets.QPushButton, 'guest')

        self.fname = self.findChild(QtWidgets.QLineEdit, 'fname')
        self.lname = self.findChild(QtWidgets.QLineEdit, 'lname')
        self.dob = self.findChild(QtWidgets.QDateEdit, 'dob')
        self.email = self.findChild(QtWidgets.QLineEdit, 'email')
        self.passwd = self.findChild(QtWidgets.QLineEdit, 'passwd')
        self.cnf_passwd = self.findChild(QtWidgets.QLineEdit, 'cnf_passwd')
        self.street = self.findChild(QtWidgets.QLineEdit, 'street')
        self.locality = self.findChild(QtWidgets.QLineEdit, 'locality')
        self.city = self.findChild(QtWidgets.QLineEdit, 'city')
        self.state = self.findChild(QtWidgets.QLineEdit, 'state')
        self.country = self.findChild(QtWidgets.QLineEdit, 'country')

        self.button1.clicked.connect(self.register)
        self.button2.clicked.connect(self.loginFun)
        self.button3.clicked.connect(self.guestFun)

    def register(self):

        f_name=self.fname.text()
        l_name=self.lname.text()
        dateofbirth=self.dob.text()
        useremail=self.email.text()
        userpasswd=self.passwd.text()
        userstreet=self.street.text()
        userlocality=self.locality.text()
        usercity=self.city.text()
        userstate=self.state.text()
        usercountry=self.country.text()

        query='INSERT INTO Student(student_f_name, student_l_name, student_dob, street_name, Locality, city, state, country, student_email, student_password, grade_id) VALUES ("'+f_name+'","'+l_name+'","'+dateofbirth+'","'+userstreet+'","'+userlocality+'","'+usercity+'","'+userstate+'","'+usercountry+'","'+useremail+'","'+userpasswd+'","1")'
        # print(query)
        cursor = db_connection.cursor()
        # # sql_statement = "SELECT * FROM Grades"
        result=cursor.execute(query)
        db_connection.commit()
        cursor.close()
        login1.loginClass.startWin(self)
        self.close()
        # output = my_database.fetchall()

        # if my_database.rowcount>0:
        #     print("logged in")
        # else:
        #     print("incorrect password")

        
    def loginFun(self):
        print("login")
        login1.loginClass.startWin(self)
        self.close()
    def guestFun(self):
        print("guest")
        dashboard.dashboard.startWin(self)
        self.close()



    def startWin(self):
        window = RegisterClass(self)
        window.showFullScreen()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = RegisterClass()
    w.showFullScreen()
    sys.exit(app.exec())