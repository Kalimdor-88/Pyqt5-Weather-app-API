from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit,QMainWindow,
                            QPushButton, QWidget, QAction,
                            QToolBar,QHBoxLayout, QDoubleSpinBox,
                            QSpinBox, QCheckBox, QSlider, QGridLayout, QComboBox, 
                            )
from PyQt5.QtGui import QPixmap, QIcon

#-----------Main Window Infrastructure--------------
class MainWindow(QMainWindow):
    def __init__(self, Page1):
        super().__init__()
        self.page1 = Page1
        self.toolbar1 = QToolBar("Click me")
        self.addToolBar(self.toolbar1)
        self.button_action = QAction(QIcon("PithonVSCODE/PyQt5_Tutorial/6.Test_QToolbar_QAction/home.png"),"Your button", self)
        self.button_action.setStatusTip("Click me to Move Things.")
        self.toolbar1.addAction(self.button_action)
        self.button_action.setCheckable(True)
        # self.setStyleSheet("background-color: blue;")
        # self.toolbar1.setMovable(False) 

        self.movethings_widget = QWidget()
        self.label1 = QLabel("LineEdit")
        self.label2 = QLabel("PushButton")
        self.label3 = QLabel("Size: ")
        self.label4 = QLabel("Positioning: ")
        self.dspinbox = QDoubleSpinBox()
        self.cbox1 = QCheckBox()
        self.cbox2 = QCheckBox()
        self.slidr = QSlider(Qt.Horizontal, self.movethings_widget)
        self.vbox_tool1 = QVBoxLayout()
        self.vbox_tool2 = QVBoxLayout()
        self.vbox_tool3 = QVBoxLayout()
        self.vbox_tool4 = QVBoxLayout()
        self.hbox_tool = QHBoxLayout()
        self.gridbox_tool1 = QGridLayout()
        self.spinbox = QSpinBox(self.movethings_widget)
        self.combBox = QComboBox()

        self.button_action.toggled.connect(self.toolbarclicked)
        self.initoolsui()
                
    def initoolsui(self):
        self.slidr.setFixedSize(170,30)
        self.movethings_widget.setFixedSize(400,200)
        self.dspinbox.setFixedSize(200,30)
        self.combBox.setFixedWidth(200)
        self.slidr.setRange(0,2000)
        self.spinbox.setMaximum(2000)

        self.combBox.setStyleSheet("font-size: 15px;")
        self.label1.setStyleSheet("font-size: 15px;")
        self.label2.setStyleSheet("font-size: 15px;")
        self.label3.setStyleSheet("font-size: 15px;")
        self.label4.setStyleSheet("font-size: 15px;")
        self.spinbox.setStyleSheet("font-size: 15px;")

        self.gridbox_tool1.addWidget(self.cbox1, 0, 2)
        self.gridbox_tool1.addWidget(self.label1, 1, 2, Qt.AlignmentFlag.AlignTop)
        self.gridbox_tool1.addWidget(self.cbox2, 0, 3)
        self.gridbox_tool1.addWidget(self.label2, 1, 3, Qt.AlignmentFlag.AlignTop)

        self.gridbox_tool1.addWidget(self.combBox, 3, 3)
        self.gridbox_tool1.addWidget(self.label4, 2, 3, Qt.AlignmentFlag.AlignBottom)

        self.gridbox_tool1.addWidget(self.slidr, 3, 2)
        self.gridbox_tool1.addWidget(self.label3,2, 2, Qt.AlignmentFlag.AlignBottom)
        self.gridbox_tool1.addWidget(self.spinbox,4, 2,Qt.AlignmentFlag.AlignTop)

        self.slidr.valueChanged.connect(lambda: self.label3.setText(f"Size: {self.slidr.value()}"))
        self.slidr.valueChanged.connect(lambda: self.spinbox.setValue(self.slidr.value()))
        self.spinbox.valueChanged.connect(lambda Value: self.slidr.setValue(Value))

        self.combBox.addItem("AlignTop")
        self.combBox.addItem("AlignBottom")
        self.combBox.addItem("AlignCenter")
        self.combBox.addItem("AlignRight")
        self.combBox.addItem("AlignLeft")
        self.movethings_widget.setLayout(self.gridbox_tool1)

        self.combBox.currentTextChanged.connect(self.alignmethod) # ⭐⭐⭐
        self.slidr.valueChanged.connect(self.slidrmethod)


    def slidrmethod(self, value):
        if self.cbox1.isChecked():
            self.page1.cityinput.setFixedWidth(value)

        if self.cbox2.isChecked():
            self.page1.getweatherbutton.setStyleSheet(f"font-size: {value}px;") #px yazmayı unutmuşum... ⭐

    def alignmethod(self, Strng):
        if self.cbox1.isChecked():
            self.page1.hbox.setAlignment(self.page1.cityinput, getattr(Qt, Strng))

        if self.cbox2.isChecked():
            self.page1.hbox.setAlignment(self.page1.getweatherbutton, getattr(Qt, Strng))
            

    def toolbarclicked(self):
        if self.button_action.isChecked():
            self.movethings_widget.show()

#-----------First Page-------------
class Page_1(QWidget):

    def __init__(self, Stack, weatherapi):
        super().__init__()
        self.weather_api = weatherapi
        self.stack = Stack
        self.cityinput = QLineEdit()
        self.getweatherbutton = QPushButton("Get Weather", self)
        self.hbox = QHBoxLayout()
        self.pixlabel = QLabel(self)
        self.pixlabel.setPixmap(QPixmap("PithonVSCODE/weatherlzone.png"))
        self.initui()

    def initui(self):
        self.pixlabel.adjustSize()
        self.pixlabel.lower()  #⭐⭐⭐⭐

        self.setWindowTitle("Hava Durumu Programi")
        self.hbox.addWidget(self.cityinput,stretch=1, alignment=Qt.AlignTop)
        self.hbox.addWidget(self.getweatherbutton, alignment=Qt.AlignTop)
        self.setLayout(self.hbox)
        
        self.cityinput.setObjectName("input")
        self.getweatherbutton.setObjectName("button")

        self.setStyleSheet("""
        QWidget            {
            color: black;
            background-color: white;
                           }
        QLabel,QPushButton{
            font-family: calibri;
            background-color: transparent;
            border: none;
                           }
        QLineEdit#input    {
            font-size: 27px;
                           }
        QPushButton#button {
            font-size: 30px;
            font-weight: bold;
                           }
        """)
        self.getweatherbutton.clicked.connect(lambda: self.stack.setCurrentIndex(1))      
        self.getweatherbutton.clicked.connect(self.city_name)

    def city_name(self):
        self.weather_api.get_data(self.cityinput.text())

    
class Page_2(QWidget): # 🍬🍬🍬 WIDGET 2 !!! 🍬🍬🍬
    def __init__(self, page1, Stack, weather_api):
        super().__init__()
        self.stack = Stack
        self.weatherapi = weather_api
        self.Page1 = page1

        self.vlayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.temperature_label = QLabel("TemperatureLabel")
        self.description_label = QLabel("DescriptionLabel")
        self.emoji_label = QLabel("EmojiLabel")
        self.push_button1 = QPushButton("Go Back")
        self.renklabel = QLabel(self)
        self.griddlayout = QGridLayout()

        self.day1 = QLabel()
        self.day2 = QLabel()
        self.day3 = QLabel()
        self.day4 = QLabel()
        self.day5 = QLabel()

        self.initui()

    def initui(self):
        self.renklabel.setGeometry(0,0,1920,1080)
        self.renklabel.lower()
        self.griddlayout.setContentsMargins(100,100,100,1)
        self.griddlayout.setSpacing(1)
        self.setLayout(self.griddlayout)

        self.griddlayout.addWidget(self.day1, 1, 1, Qt.AlignTop)
        self.griddlayout.addWidget(self.day2, 1, 2, Qt.AlignTop)
        self.griddlayout.addWidget(self.day3, 1, 3, Qt.AlignTop)
        self.griddlayout.addWidget(self.day4, 1, 4, Qt.AlignTop)
        self.griddlayout.addWidget(self.day5, 1, 5, Qt.AlignTop)
        self.griddlayout.addWidget(self.push_button1, 2, 5)

        self.griddlayout.addWidget(self.temperature_label, 2, 1)
        self.griddlayout.addWidget(self.description_label, 2, 2)
        self.griddlayout.addWidget(self.emoji_label, 2, 3)

        self.temperature_label.hide()
        self.description_label.hide()
        self.emoji_label.hide()

        self.temperature_label.setObjectName("temperature")
        self.description_label.setObjectName("description")
        self.emoji_label.setObjectName("emoji")

        self.push_button1.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        self.setStyleSheet("""
        QWidget           {
            color: black;
            background-color: cyan;
                           }
        QLabel             {
            font-family: calibri;
            font-size: 25px;
                           }
        QPushButton        {
            font-family: calibri;
            background-color: red;
            font-weight: bold;
            font-size: 20px;
                           }
        QLabel#temperature {
            font-size: 35px;
            font-weight: bold;
                           }
        QLabel#description {
            font-size: 27px;
                           }
        QLabel#emoji       {
            font-size: 50px;
            font-family: Segoe UI emoji;
                           }
        """)

        self.weatherapi.signaldict.connect(self.display_weather)
        self.weatherapi.signalstr.connect(self.display_error)  # ⭐⭐⭐
    
    def display_error(self, message):
        print ("display_error")
        self.day1.hide()
        self.day2.hide()
        self.day3.hide()
        self.day4.hide()
        self.day5.hide()

        self.temperature_label.show()
        self.description_label.show()
        self.emoji_label.show()

        self.emoji_label.clear()
        self.description_label.clear()
        self.temperature_label.setStyleSheet("font-size: 23px;")
        self.temperature_label.setText(message)


    def display_weather(self, data):
        print ("display_weather")
        self.day1.show()
        self.day2.show()
        self.day3.show()
        self.day4.show()
        self.day5.show()

        self.temperature_label.hide()
        self.description_label.hide()
        self.emoji_label.hide()

        print("received in:", self.Page1)
        self.temperature_label.setStyleSheet("font-size: 35px;")

        weather_id1 = data["list"][4]["weather"][0]["id"]
        weather_id2 = data["list"][12]["weather"][0]["id"]
        weather_id3 = data["list"][20]["weather"][0]["id"]
        weather_id4 = data["list"][28]["weather"][0]["id"]
        weather_id5 = data["list"][36]["weather"][0]["id"]


        temperat_k1 = data["list"][4]["main"]["temp"] - 273.15  
        temperat_k2 = data["list"][12]["main"]["temp"] - 273.15
        temperat_k3 = data["list"][20]["main"]["temp"] - 273.15
        temperat_k4 = data["list"][28]["main"]["temp"] - 273.15
        temperat_k5 = data["list"][36]["main"]["temp"] - 273.15


        self.day1.setText(f"{data['list'][4]['weather'][0]['main']} \n {self.get_weather_emoji(weather_id1)} \n {temperat_k1:.1f}°C")
        self.day2.setText(f"{data['list'][12]['weather'][0]['main']} \n {self.get_weather_emoji(weather_id2)} \n {temperat_k2:.1f}°C")
        self.day3.setText(f"{data['list'][20]['weather'][0]['main']} \n {self.get_weather_emoji(weather_id3)} \n {temperat_k3:.1f}°C")
        self.day4.setText(f"{data['list'][28]['weather'][0]['main']} \n {self.get_weather_emoji(weather_id4)} \n {temperat_k4:.1f}°C")
        self.day5.setText(f"{data['list'][36]['weather'][0]['main']} \n {self.get_weather_emoji(weather_id5)} \n {temperat_k5:.1f}°C")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <=232:
            return 	"🌩️"
        elif 300 <= weather_id <=321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 751 or weather_id == 761 or weather_id == 771 or weather_id == 781:
            return "🌪️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        

     