import requests
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from bs4 import BeautifulSoup
from screeninfo import get_monitors
import os
import sys

import ctypes
from ctypes import wintypes as w



try:
    imgList = []
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
        #add current wallpaper to imgList
        image = SysFuncs.get_wallpaper(self)
        imgList.append(image)
        print(imgList)

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
        imgList.append(name)

        print(imgList)



    def prevImage(self):
        imgList.pop()
        #last_element = imgList[-1]
        SysFuncs.set_wallpaper(self, temp + imgList[-1])
        #print(imgList)


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
        url = "https://wallhaven.cc/search?q=id:37&sorting=random&ref=fp"
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



class SysFuncs():
    def get_resolution(self):
        for m in get_monitors():
            return m.width, m.height

    def set_wallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path+".jpg", 0)

    def get_wallpaper(self):
        SPI_GETDESKWALLPAPER = 0x0073

        dll = ctypes.WinDLL('user32')
        dll.SystemParametersInfoW.argtypes = w.UINT, w.UINT, w.LPVOID, w.UINT
        dll.SystemParametersInfoW.restype = w.BOOL

        path = ctypes.create_unicode_buffer(260)
        result = dll.SystemParametersInfoW(SPI_GETDESKWALLPAPER, ctypes.sizeof(path), path, 0)
        print(path.value)
        if result == True:
            return path.value
        else:
            return "Error"



    def checkNet(self):
        try:
            response = requests.get("http://www.google.com")
            return True
        except requests.ConnectionError:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
