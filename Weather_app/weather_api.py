from PyQt5.QtCore import QObject, pyqtSignal

import requests

# from ui import MainWindow
from config import api_key

class WeatherApi(QObject):
    signaldict = pyqtSignal(dict)
    signalstr = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
    def get_data(self, cityinput):
        print("emit from:" + cityinput)
        if cityinput:
            print (cityinput)
            city_name = cityinput
        
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}")
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200:
                self.signaldict.emit(data)
                # print (data["list"][3]["weather"][0]["main"])

        except UnboundLocalError:
            self.signalstr.emit("Please Enter a City name")
                                
        # except requests.exceptions.HTTPError as http_error:
        #     self.signalstr.emit(http_error)

        except TypeError:
            self.signalstr.emit("Please Enter a City name")

        except requests.exceptions.ConnectionError:
            self.signalstr.emit("Connection-Error:\nPlease check your internet connection. ")
        except requests.exceptions.ConnectTimeout:
            self.signalstr.emit("Connect-Timeout:\nConnection timed out. Please Try again. ")
        except requests.exceptions.TooManyRedirects:
            self.signalstr.emit("Too-Many-Redirects:\nPlease check your URL. ")
        except requests.exceptions.RequestException as req_error:
            self.signalstr.emit(f"A Request error occured:\n{req_error}")

    def display_httpErr(self, statcode):
        match statcode:
            case 400:
                self.signalstr.emit("400-Bad-Request:\nPlease check your input.")
            case 401:
                self.signalstr.emit("401-Unauthorized:\nUnvalid API key. ")
            case 403:
                self.signalstr.emit("403-Forbidden:\nAccess is denied.")
            case 404:
                self.signalstr.emit("404-Not-Found:\nCity Not Found")
            case 500:
                self.signalstr.emit("500-Internal-Server-Error:\nServer is down. Please try again later.")
            case 502:
                self.signalstr.emit("502-Bad-Gateway:\nInvalid response from the server. ")
            case 503:
                self.signalstr.emit("503-Service-Unavailable:\nServer is down. Please try again later. ")
            case 504:
                self.signalstr.emit("504-Gateway-Timeout:\nNo Response from the server. ")
            case _:
                self.signalstr.emit(f"An error occured\n{statcode}")