#!/usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import division
import os
import sys
import zipfile
import threading
from jnius import cast
from jnius import autoclass
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest


ver_check = 'http://defendergr.000webhostapp.com/dvm.ver'
ver_filename = os.path.join(os.environ['EXTERNAL_STORAGE'], "Android/data/org.xbmc.kodi/files/.kodi/rdvm.ver")
ZIP_URL = 'http://defendergr.000webhostapp.com/DVMod.zip'
ZIP_UPDATE_URL = 'http://defendergr.000webhostapp.com/DVModUpdate.zip'
ZIP_FIX = 'http://defendergr.000webhostapp.com/DVModFix.zip'
ZIP_FILENAME = 'DVMod.zip'
ZIP_EXTRACT_FOLDER = os.path.join(os.environ['EXTERNAL_STORAGE'], "Android/data/org.xbmc.kodi/files/.kodi")
lfile = os.path.join(os.environ['EXTERNAL_STORAGE'], "Android/data/org.xbmc.kodi/files/.kodi/dvm.ver")


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
        Label:
            markup: True
            color: 0.5, 0.5, 0.5, 1.0
            bgcolor: 0.0, 0.6, 0.6, 1.0
            size_hint: 0.7, 0.4
            pos_hint: {'center_x': 0.5}
            id: msg
            font_size: 100
            text:'[b]dokimi[/b]'
        Button:
            background_normal: ''
            background_color: (0.0, 0.6, 0.6, 1.0)
            opacity: 1.0
            size_hint: 0.7, 0.5
            pos_hint: {'center_x': 0.5}
            id: download_button
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
            text: "Έξοδος"
            on_press: self.parent.parent.exit()
"""
Builder.load_string(kv_string)


class RootWidget(BoxLayout):
    '''main app class'''
    stop = threading.Event()

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def download_content(self):
        '''Zip Download'''
        if MyApp.localver == MyApp.remotever:
            self.ids["download_button"].disabled = True
            self.ids["download_button"].text = 'Φώρτοση...'
            RootWidget.start_kodi()
        elif MyApp.CHECK:
            self.ids["download_button"].disabled = True
            self.ids["download_button"].text = 'Λήψη αναβάθμισης του DVMod'
            UrlRequest(ZIP_UPDATE_URL, on_progress=self.update_progress, chunk_size=1024, on_success=self.unzip_content, file_path=ZIP_FILENAME)
        else:
            self.ids["download_button"].disabled = True
            self.ids["download_button"].text = 'Λήψη... DVMod'
            UrlRequest(ZIP_URL, on_progress=self.update_progress, chunk_size=1024, on_success=self.unzip_content, file_path=ZIP_FILENAME)

    def update_progress(self, request, current_size, total_size):
        '''Progress Bar'''
        self.ids['download_progress_bar'].value = current_size / total_size
        self.ids['download_button'].text = 'Λήψη... '+str(int(current_size/1024**2))+'MB από '+str(int(total_size/1024**2))+'MB (' + str(int((current_size / total_size)/0.01))+ '%)'

    def unzip_content(self, req, result):
        '''starting unzip'''
        threading.Thread(target=self.unzip_thread).start()
        sys.exit()

    def unzip_thread(self):
        '''Unzip File'''
        self.ids["download_button"].text = 'Εγκατάσταση του DVMod'
        fh = open(ZIP_FILENAME, 'rb')
        z = zipfile.ZipFile(fh)
        if not os.path.exists(ZIP_EXTRACT_FOLDER):
            os.makedirs(ZIP_EXTRACT_FOLDER)
        z.extractall(ZIP_EXTRACT_FOLDER)
        fh.close()
        os.remove(ZIP_FILENAME)
        self.ids["download_button"].text = 'Φώρτοση...'
        self.ids["download_button"].disabled = True
        RootWidget.start_kodi()

    @staticmethod
    def start_kodi():
        '''starts kodi app'''
        app_to_launch = "org.xbmc.kodi"
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = cast('android.app.Activity', PythonActivity.mActivity)
        pm = activity.getPackageManager()
        app_intent = pm.getLaunchIntentForPackage(app_to_launch)
        activity.startActivity(app_intent)
        sys.exit()

    def exit_content(self):
        '''exit button'''
        self.ids["download_button"].disabled = True
        MyApp.localver.close()
        MyApp.remotever.close()
        os.remove(ver_filename)
        sys.exit()


class MyApp(App):
    '''DVMod Check remote & local version'''
    CHECK = os.path.isfile(os.path.join(os.environ['EXTERNAL_STORAGE'], "Android/data/org.xbmc.kodi/files/.kodi/dvm.ver"))
    req = UrlRequest(ver_check, file_path=ver_filename)

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
    elif CHECK:
        text = "Αναβάθμιση του DVMod"
    else:
        text = "Λήψη και εγκατάσταση του DVMod"

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MyApp().run()
