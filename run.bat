@echo off
setlocal enabledelayedexpansion
echo [Wallpaper] Loading...


if not exist "python\" (
	echo [Wallpaper] Python is not installed
	
	echo [Wallpaper] Python is installing...
	downloader\aria2c.exe "https://www.python.org/ftp/python/3.9.13/python-3.9.13-embed-amd64.zip" -o "python.zip"
	
	md python
	tar -xf python.zip -C python
	del python.zip
	(
		echo python39.zip
		echo .
		echo import site
	)>>"python\python39._pth"

    downloader\aria2c.exe "https://bootstrap.pypa.io/get-pip.py" -o "python\get-pip.py"
	python\python.exe python\get-pip.py

	echo [Wallpaper] Python is installed
	
)


python\Scripts\pip.exe install -r requirements\windows_requirements.txt
start python\pythonw.exe src\main.pyw

echo [Wallpaper] The program must be in tray
