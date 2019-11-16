import os
import sys
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
import mysql.connector
import register
import urllib.request, json 
import wolframalpha


import xml.etree.ElementTree as ET

db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="Edudroid"
)


class dashboard(QtWidgets.QDialog):
    
    def __init__(self, parent=None):

        my_database = db_connection.cursor()
        sql_statement = "SELECT * FROM history"
        my_database.execute(sql_statement)
        output = my_database.fetchall()

        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "Layout/dashboard.ui"),self)

        self.searchButton=self.findChild(QtWidgets.QPushButton,'searchButton')
        self.searchBar=self.findChild(QtWidgets.QLineEdit,'searchBar')

        self.searchButton.clicked.connect(self.searchFun)

        self.outputText=self.findChild(QtWidgets.QLabel,'outputText')
        self.outputImage=self.findChild(QtWidgets.QLabel,'outputImage')

        self.historyList=self.findChild(QtWidgets.QListWidget,'history')
        self.recommendedList=self.findChild(QtWidgets.QListWidget,'recommended')
        self.pastList=self.findChild(QtWidgets.QListWidget,'past')
        y=1
        for x in output:
            y+=1
            item = QListWidgetItem(self.historyList)
            # CustomQWidget.setValue(str(output),y)
            item_widget = CustomQWidget(str(x),y)
            item.setSizeHint(item_widget.sizeHint())
            self.historyList.addItem(item)
            self.historyList.setItemWidget(item, item_widget) 

        with urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?key=AIzaSyD7uGpVUCHq90oIVQbK4ta_oETx7jaCPPQ&channelId=UC4a-Gbdw7vOaccHmFo40b9g&part=snippet,id&order=date&maxResults=20") as url:
            data = json.loads(url.read().decode())
            
            apiitems=data['items']
            for x,y in list(enumerate(apiitems)):
                snippetItem=apiitems[x]['snippet']
                thumbnailItem=snippetItem['thumbnails']
                mediumImage=thumbnailItem['default']
                imageUrl=mediumImage['url']
                # print(imageUrl)
                imageHeight=mediumImage['height']
                imageWidth=mediumImage['width']
                # print(mediumImage)
                # self.recommendedList.addItem(snippetItem['title'])
                item = QListWidgetItem(self.recommendedList)
                # # CustomQWidget.setValue(str(output),y)
                item_widget = YoutubeQWidget(snippetItem['title'],x,imageUrl,imageWidth,imageHeight)
                item.setSizeHint(item_widget.sizeHint())
                self.recommendedList.addItem(item)
                self.recommendedList.setItemWidget(item, item_widget)

    def searchFun(self):
        app_id="Q933QV-JA44G6RA9J"
        client=wolframalpha.Client(app_id)
        searchQuery=self.searchBar.text()
        res=client.query(searchQuery)
        for pod in res.pods:
            podList=list(pod.values())
            #podList[1]-for input and plot
            #podList[6] - info
            if podList[1]=='Plotter':
                finalImg=(((podList[6])[1])['img'])['@src']
            elif podList[1]=='Reduce':
                finalImg=((podList[6])['img'])['@src']
            else:
                finalImg=(((podList[6])[1])['img'])['@src']
            
            if podList[1]=='Identity':
                if str(type(podList[6])) == "<class 'dict'>":
                    print((podList[6])['plaintext'])
                    # finalOutput=intvalue['plaintext']
                    finalOutput=(podList[6])['plaintext']
            

        query="INSERT INTO history(history_formula, history_solution) VALUES ('"+searchQuery+"','"+finalOutput+"')"
        # print(query)
        cursor = db_connection.cursor()
        result=cursor.execute(query)
        db_connection.commit()
        cursor.close()

        pixmap=QPixmap()
        data = urllib.request.urlopen(finalImg).read()
        pixmap.loadFromData(data)
        self.outputImage.setPixmap(pixmap)

        self.outputText.setText(finalOutput)
        print('Button workin')
        self.update()

    def startWin(self):
        window = dashboard(self)
        window.showFullScreen()

class CustomQWidget(QtWidgets.QWidget):
    def __init__(self, courseCode_temp,grade_temp,parent=None):
        super(CustomQWidget, self).__init__(parent)
        label = QLabel(str(courseCode_temp))
        button = QPushButton(str(grade_temp))
        # print(grade_temp)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)

class YoutubeQWidget(QtWidgets.QWidget):
    def __init__(self, youtubeTitle,YoutubeLink,imageLink,imageSizeW,imageSizeH,parent=None):
        super(YoutubeQWidget, self).__init__(parent)
        labelimg = QLabel(self)
        pixmap = QPixmap()
        data = urllib.request.urlopen(imageLink).read()
        pixmap.loadFromData(data)
        labelimg.setPixmap(pixmap)

        # Optional, resize window to image size
        self.resize(pixmap.width(),pixmap.height())
        
        label = QLabel(str(youtubeTitle))
        label.setWordWrap(1)
        label.setFixedWidth(150)
        label.setStyleSheet('text-align:left')
        button = QPushButton('play')
        button.setFixedWidth(100)
        # print(grade_temp)
        layout = QHBoxLayout()
        layout.setSizeConstraint(100)
        layout.addWidget(labelimg)
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = dashboard()
    w.showFullScreen()
    sys.exit(app.exec())