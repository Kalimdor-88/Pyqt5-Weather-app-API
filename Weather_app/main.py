from PyQt5.QtWidgets import (QApplication, QTabWidget)                            

from ui import Page_1, Page_2, MainWindow
from weather_api import WeatherApi

if __name__ == "__main__":
    program = QApplication([])
    stack = QTabWidget()

    stack.setTabPosition(QTabWidget.North)
    stack.setStyleSheet("font-size: 24px;")

    weatherapi = WeatherApi()
    page1 = Page_1(stack, weatherapi)
    mainwindow = MainWindow(page1)
    page2 = Page_2(page1, stack, weatherapi)

    stack.addTab(page1,"Home")
    stack.addTab(page2, "Weather")
    
    mainwindow.setCentralWidget(stack)
    mainwindow.show()
    program.exec_()
