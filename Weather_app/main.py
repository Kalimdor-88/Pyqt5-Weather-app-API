import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit,
                            QPushButton, QWidget, QApplication)
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ilkmesaj = QLabel("Enter a city:",self)
        self.cityinput = QLineEdit(self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.getweatherbutton = QPushButton("Get Weather",self)
        self.initui()

    def initui(self):
        self.setWindowTitle("Weather App Program")
        vbox = QVBoxLayout()
        vbox.addWidget(self.ilkmesaj)
        vbox.addWidget(self.cityinput)
        vbox.addWidget(self.getweatherbutton)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.emoji_label)
        self.setLayout(vbox)

        self.ilkmesaj.setAlignment(Qt.AlignCenter)
        self.cityinput.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.ilkmesaj.setObjectName("mesaj")
        self.cityinput.setObjectName("input")
        self.temperature_label.setObjectName("temperature")
        self.description_label.setObjectName("description")
        self.getweatherbutton.setObjectName("button")
        self.emoji_label.setObjectName("emoji")

        self.setStyleSheet("""
        QLabel,QPushButton{
            font-family: calibri;
                           }
        QLabel#mesaj{
            font-size: 30px;
            font-style: italic;
                           }
        QLineEdit#input{
            font-size: 20px;
                           }
        QLabel#temperature{
            font-size: 35px;
            font-weight: bold;
                           }
        QLabel#description{
            font-size: 27px;
                           }
        QPushButton#button{
            font-size: 34px;
            font-weight: bold;
                           }
        QLabel#emoji{
            font-size: 43px;
            font-family: Segoe UI emoji;
                           }
        """)

        self.getweatherbutton.clicked.connect(self.get_weather)

    def get_weather(self):
        city_name = self.cityinput.text()
        api_key = "your own api-key, copy-paste here" # you need to enter your own api-key from https://openweathermap.org/api
        response1 = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}")
        try:
            response1.raise_for_status() # HTTP error yakalaması için bu şart.
            data_ilk = response1.json()
            lat = data_ilk[0]["lat"]
            lon = data_ilk[0]["lon"]        
            response2 = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}")
            response2.raise_for_status()  # HTTP error yakalaması için bu şart.
            stat_code = response1.status_code
            data_son = response2.json()
            weather_descript = data_son["weather"][0]["description"]
            weather_id = data_son["weather"][0]["id"]
            self.display_weather(data_son)
            if stat_code == 200:
                self.description_label.setText(weather_descript)
                self.emoji_label.setText(self.display_emoji(weather_id))
        except IndexError:
            self.display_error("Hatali tuşlama.")
        except requests.exceptions.HTTPError as http_err:   
            WeatherApp.error_message(response1.status_code)
        except requests.exceptions.ConnectionError:
            self.display_error("Connection-Error:\nPlease check your internet connection. ")
        except requests.exceptions.ConnectTimeout:
            self.display_error("Connect-Timeout:\nConnection timed out. Please Try again. ")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too-Many-Redirects:\nPlease check your URL. ")
        except requests.exceptions.RequestException:
            self.display_error(f"A Request error occured:\n{http_err}")
    def display_error(self,message):            
        self.temperature_label.setText(message)
    def error_message(self,stat_code):
        match stat_code:
            case x if x // 100 == 3:
                self.display_error("Redirection issues,\nPlease try again later.")
            case x if x // 100 == 4:
                self.display_error("Client issues,\nMight be due to missinput or unauthorized api-key.")
            case x if x // 100 == 5:
                self.display_error("Server issues,\nThis error is due to server-side\nPlease try again later.")    
    def display_weather(self, data_son):
        tempk = data_son["main"]["temp"]
        tempc = tempk -273.15
        tempf = (tempk * 9/5) - 459.67
        self.temperature_label.setText(f"{tempc:.01f}°C")
    @staticmethod
    def display_emoji(weather_id):
        match weather_id:
            case _ if 200 <= weather_id <= 232: 
                return "⛈️"
            case x if 300 <= x <= 321:
                return  "🌦️"
            case x if 500 <= x <= 531:
                return  "🌧️"
            case x if 600 <= x <= 622:
                return  "❄️"
            case x if 701 <= x <= 741:
                return  "🌫️"
            case 751 | 761 | 771 | 781:
                return  "🌪️"
            case 762:
                return  "🌋"
            case 800:
                return  "🌞"
            case x if 801 <= x <= 804:
                return  "☁️"
            case _:
                return ""

if __name__ == "__main__":
    program = QApplication(sys.argv)
    havadurumu_programi = WeatherApp()
    havadurumu_programi.show()
    sys.exit(program.exec_())