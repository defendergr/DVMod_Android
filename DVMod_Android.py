#!/usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import division
from os import path
from os import environ
from os import system
from os import makedirs
from sys import exit
from os import remove
import zipfile
import threading
#import time
#import errno
#import stat
#import shutil
#from jnius import cast
#from jnius import autoclass
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.uix.progressbar import ProgressBar
from kivy.context import get_current_context
from kivy import Config
import kivy.uix.behaviors.focus
Config.set('graphics', 'multisamples', '0')


#image = 'http://defendergr.000webhostapp.com/image.jpg'
#image_filename = image.jpg
ver_check = 'http://defendergr.000webhostapp.com/dvm.ver'
ver_filename = path.join(environ['APPDATA'], "Kodi/rdvm.ver")
ZIP_URL = 'http://defendergr.000webhostapp.com/DVMod.zip'
ZIP_UPDATE_URL = 'http://defendergr.000webhostapp.com/DVModUpdate.zip'
ZIP_FIX = 'http://defendergr.000webhostapp.com/DVModFix.zip'
ZIP_FILENAME = 'DVMod.zip'
ZIP_EXTRACT_FOLDER = path.join(environ['APPDATA'], "Kodi/")
#download_progress_bar = ProgressBar
lfile = path.join(environ['APPDATA'], "Kodi/dvm.ver")


# system check
#if sys.platform == "win32":
#    ZIP_EXTRACT_FOLDER = os.path.join(os.environ['APPDATA'], "Kodi")
#    print("Defender's Video Mod", "\n", "installation for Windows has started", "\n", "Please Wait...")
#elif sys.platform == "linux":
#    ZIP_EXTRACT_FOLDER = os.path.join(os.environ['EXTERNAL_STORAGE'], "Android/data/org.xbmc.kodi/files/.kodi")
#    print("Defender's Video Mod", "\n", "installation for Android has started", "\n", "Please Wait...")
#else:
#    print("Sorry, we don't currently have support for the " + sys.platform + " OS")
#    sys.exit()


# interface
kv_string = """
<RootWidget>
    canvas:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            source: 'image.jpg'
            size: self.size
    BoxLayout:
        orientation: "vertical"
        size_hint: 0.8, 0.2
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        Button:
        	background_normal: ''
        	background_color: (0.0, 0.6, 0.6, 1.0)
        	opacity: 1.0
        	size_hint: 0.7, 0.4
        	pos_hint: {'center_x': 0.5}
            id: download_button
            focus: True
            text: app.text
            on_press: self.parent.parent.download_content()
        ProgressBar:
        	opacity: 1.0
        	size_hint: 0.7, 0.3
        	pos_hint: {'center_x': 0.5}
            id: download_progress_bar
            max: 1
            value: 0
        Button:
        	opacity: 1.0
        	size_hint: 0.3, 0.3
        	pos_hint: {'center_x': 0.5}
            id: exit_button
            focus: False
            text: "Έξοδος"
            on_press: self.parent.parent.exit_content()
"""
Builder.load_string(kv_string)


class RootWidget(BoxLayout):
    stop = threading.Event()

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)


# Zip Download
    def download_content(self):
    	if MyApp.aline < 600 and MyApp.CHECK or MyApp.line == MyApp.line2:
            self.ids["download_button"].disabled = True
            self.ids["download_button"].text = 'Φώρτοση...'
            req = UrlRequest(ZIP_FIX, on_progress=self.update_progress, chunk_size=1024, on_success=self.unzip_content, file_path=ZIP_FILENAME)
    	elif MyApp.localver == MyApp.remotever:
            self.ids["download_button"].disabled = True
            self.ids["download_button"].text = 'Φώρτοση...'
            RootWidget.start_kodi(self) 
    	elif MyApp.CHECK== True:
    		self.ids["download_button"].disabled = True
    		self.ids["download_button"].text = 'Λήψη αναβάθμισης του DVMod'
    		req = UrlRequest(ZIP_UPDATE_URL, on_progress=self.update_progress, chunk_size=1024, on_success=self.unzip_content, file_path=ZIP_FILENAME)
    	else:
            self.ids["download_button"].disabled = True
            self.ids["download_button"].text = 'Λήψη... DVMod'
            req = UrlRequest(ZIP_URL, on_progress=self.update_progress, chunk_size=1024, on_success=self.unzip_content, file_path=ZIP_FILENAME)

# Progress Bar
    def update_progress(self, request, current_size, total_size):
        self.ids['download_progress_bar'].value = current_size / total_size
        self.ids["download_button"].text = 'Λήψη... '+str(int(current_size/1024**2))+'MB από '+str(int(total_size/1024**2))+'MB ('+str(int((current_size / total_size)/0.01))+'%)'

# Unzip File
    def unzip_content(self, req, result):
        threading.Thread(target=self.unzip_thread).start()
#        sys.exit()

# Unzip File
    def unzip_thread(self):
    	self.ids["download_button"].text = 'Εγκατάσταση του DVMod'
    	fh = open(ZIP_FILENAME, 'rb')
    	z = zipfile.ZipFile(fh)
    	if not path.exists(ZIP_EXTRACT_FOLDER):
    		makedirs(ZIP_EXTRACT_FOLDER,0o755)
    	z.extractall(ZIP_EXTRACT_FOLDER)
    	fh.close()
    	remove(ZIP_FILENAME)
    	self.ids["download_button"].text = 'Φώρτοση...'
    	self.ids["download_button"].disabled = True
    	RootWidget.start_kodi(self)

    def start_kodi(self):
        system('"C:\PROGRA~1"\Kodi\kodi.exe')
#    	app_to_launch = "org.xbmc.kodi"
#    	PythonActivity = autoclass('org.renpy.android.PythonActivity')
#    	activity = cast('android.app.Activity', PythonActivity.mActivity)
#    	pm = activity.getPackageManager()
#    	app_intent = pm.getLaunchIntentForPackage(app_to_launch)
#    	activity.startActivity(app_intent)
        exit(0)

# exit button
    def exit_content(self):
        self.ids["download_button"].disabled = True
#        os.close(MyApp.localver)
#        os.close(MyApp.remotever)
        exit(0)


class MyApp(App):
# DVMod Check remote & local version
	CHECK = path.join(environ['APPDATA'], "Kodi/dvm.ver")
	req = UrlRequest(ver_check, file_path=ver_filename)
#	req = UrlRequest(image, file_path='image.jpg')
	CHECK_FIX = path.join(environ['APPDATA'], "Kodi/UserData/guisettings.xml")
	line2 = (b'    <setting id="lookandfeel.skin" default="true">skin.estuary</setting>\n')
	print(line2)
	CHECK_FIX2 = path.join(environ['APPDATA'], "Kodi/UserData/addon_data/skin.amber/settings.xml")
	
	try:
		f = open (CHECK_FIX, 'rb')
		lines = f.readlines()
		line = lines[96]
		print(line)
		f2 = open (CHECK_FIX2, 'rb')
		lines2 = f2.readlines()
		aline = len(lines2)
		print(aline)
	except:
		line = False
		aline = False

	try:
		req
		localver = open(lfile, 'rb').read()
		remotever = open(ver_filename, 'rb').read()
	except:
		req
		localver = None
		remotever = False

	if localver == remotever:
		text = "Άνοιγμα"
	elif CHECK == True:
		text = "Αναβάθμιση του DVMod"
	else:
		text = "Λήψη και εγκατάσταση του DVMod"	
	
	
	def build(self):
		return RootWidget()


if __name__ == '__main__':
    MyApp().run()