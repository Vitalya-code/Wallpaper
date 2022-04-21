from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
import sys
import requests
from bs4 import BeautifulSoup
from screeninfo import get_monitors
import os
import ctypes

try:
    temp = os.getenv("temp")
    #print(temp)
    os.mkdir(temp + "\Wallpapers")
    temp = temp+r"\Wallpapers\ "

except:
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # TrayIcon
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("ico.ico"))
        self.tray.setVisible(True)

        # trayMenu
        self.menu = QMenu(self)

        self.nextImage = QAction("Next image")
        self.prevImage = QAction("Previous image")
        self.settings = QAction("Settings")
        self.quit = QAction("Quit")

        self.nextImage.triggered.connect(Buttons.nextImage)
        self.prevImage.triggered.connect(Buttons.prevImage)
        #self.settings.triggered.connect(Buttons.settings)
        self.quit.triggered.connect(app.quit)

        self.menu.addAction(self.nextImage)
        self.menu.addAction(self.prevImage)
        #self.menu.addAction(self.settings)
        self.menu.addAction(self.quit)
        self.tray.setContextMenu(self.menu)

        app.exec()


class Buttons():
    def nextImage(self):
        url, name = Parsing.getImageUrl(self)
        Parsing.imageDownload(self, url, name)
        SysFuncs.set_wallpaper(self, temp+name)

    def prevImage(self):
        print("prevImage")

    #def settings(self):
        #print("settings")

class Parsing():
    def imageDownload(self, url, name):

        #print(temp + name + ".jpg")


        response = requests.get(url)
        file = open(temp + name + ".jpg", "wb")
        file.write(response.content)
        file.close()


    def getImageUrl(self):
        #url = 'https://wallhaven.cc/search?sorting=random&ref=fp'
        url = "https://wallhaven.cc/search?sorting=random&ref=fp"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('a', class_="preview")

        for i in quotes:
            url = requests.get(i['href'])
            soup = BeautifulSoup(url.text, 'lxml')
            parsed = soup.find('img', id="wallpaper")

            width, height = SysFuncs.get_resolution(self)
            if int(parsed['data-wallpaper-width']) >= int(width) and int(parsed['data-wallpaper-height']) >= int(height):
                return parsed["src"], parsed["alt"]



    def checkNet(self):
        try:
            response = requests.get("http://www.google.com")
            return True
        except requests.ConnectionError:
            return False


class SysFuncs():
    def get_resolution(self):
        for m in get_monitors():
            return m.width, m.height

    def set_wallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path+".jpg", 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
