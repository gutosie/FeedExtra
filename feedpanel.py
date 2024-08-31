# -*- coding: utf-8 -*-
########################################
####        all-forum.cba.pl        ####
########################################
from __future__ import absolute_import, print_function
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.ConfigList import ConfigListScreen
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, NoSave
from enigma import eTimer
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen, path as os_path
from os.path import dirname, isdir, isdir as os_isdir
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, createDir
from Tools.Downloader import downloadWithProgress
from twisted.web.client import getPage
import os
PLUGINVERSION = '1.39'

class BoundFunction():
    __module__ = __name__

    def __init__(self, fnc, *args):
        self.fnc = fnc
        self.args = args

    def __call__(self):
        self.fnc(*self.args)


class mainboard(Screen):
    skin = '\n<screen name="module" position="center,center" size="760,570" flags="wfNoBorder" title="Panel Extra">\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pos.png" alphatest="blend" position="697,107" size="24,355" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,108" size="680,353" zPosition="2" backgroundColor="#00191919" foregroundColor="#00ffffff" backgroundColorSelected="#00000000" foregroundColorSelected="#0000ffff" scrollbarMode="showOnDemand" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="2" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/logos.png" position="40,29" alphatest="blend" size="400,32" zPosition="3" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ver.png" position="615,22" alphatest="blend" size="120,45" zPosition="3" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updatePlatform()
        self.updateLib()
        self.updatePanel()
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {
         'red': self.exitPlugin,
         'green': self.update,
         'ok': self.update,
         'back': self.exitPlugin})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Airly'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootvideo'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Emu Manager'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('E2iPlayer'), png, 4)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('MediaPortal'), png, 5)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('NeoBoot'), png, 6)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('AdvancedFree Player'), png, 7)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('FreeCCcam'), png, 8)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
#        res = (_('FreeServer'), png, 9)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
        res = (_('Zoom free server Downloader'), png, 10)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('s4aUpdater'), png, 11)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('SHOUTcast'), png, 12)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Image Downloader'), png, 13)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('DreamOSat keyUpdater'), png, 14)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('J00zek Bouquets'), png, 15)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('m3uPlayer'), png, 16)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('UserSkin Setup'), png, 17)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz skin dla image ...'), png, 18)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Lcd4linux'), png, 19)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Chocholousek picons'), png, 20)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
#        res = (_('PiconManager (mod)'), png, 21)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
#        res = (_('ClearMem'), png, 22)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
#        res = (_('Mount Manager'), png, 23)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
        res = (_('ExtNumberZap'), png, 24)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('MenuSort'), png, 25)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('PluginSort'), png, 26)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
#        res = (_('RaedQuickSignal'), png, 27)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
        res = (_('AJPanel'), png, 28)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('DreamSat Panel'), png, 29)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Levi45 Addon Manager'), png, 30)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
#        res = (_('TSpanel'), png, 31)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
        res = (_('SatVenus Panel'), png, 32)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('HistoryZapSelector'), png, 33)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Internet SpeedTest'), png, 34)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('CI+ Install'), png, 35)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
#        res = (_('DreamOSat keyUpdater'), png, 36)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
#        png = LoadPixmap(mypixmap)
        res = (_('Ncam Status'), png, 37)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Oscam Status'), png, 38)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('PermanentClock 0.1'), png, 39)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('TheWeather'), png, 40)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('YouTube'), png, 41)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(board0):
            pass
        if self.sel == 1 and self.session.open(board1):
            pass
        if self.sel == 2 and self.session.open(board2):
            pass
        if self.sel == 3 and self.session.open(board3):
            pass
        if self.sel == 4 and self.session.open(board4):
            pass
        if self.sel == 5 and self.session.open(board5):
            pass
        if self.sel == 6 and self.session.open(board6):
            pass
        if self.sel == 7 and self.session.open(board7):
            pass
        if self.sel == 8 and self.session.open(board8):
            pass
        if self.sel == 9 and self.session.open(board9):
            pass
        if self.sel == 10 and self.session.open(board10):
            pass
        if self.sel == 11 and self.session.open(board11):
            pass
        if self.sel == 12 and self.session.open(board12):
            pass
        if self.sel == 13 and self.session.open(board13):
            pass
        if self.sel == 14 and self.session.open(board14):
            pass
        if self.sel == 15 and self.session.open(board15):
            pass
        if self.sel == 16 and self.session.open(board16):
            pass
        if self.sel == 17 and self.session.open(board17):
            pass
        if self.sel == 18 and self.session.open(board18):
            pass
        if self.sel == 19 and self.session.open(board19):
            pass
        if self.sel == 20 and self.session.open(board20):
            pass
        if self.sel == 21 and self.session.open(board21):
            pass
        if self.sel == 22 and self.session.open(board22):
            pass
        if self.sel == 23 and self.session.open(board23):
            pass
        if self.sel == 24 and self.session.open(board24):
            pass
        if self.sel == 25 and self.session.open(board25):
            pass
        if self.sel == 26 and self.session.open(board26):
            pass
        if self.sel == 27 and self.session.open(board27):
            pass
        if self.sel == 28 and self.session.open(board28):
            pass
        if self.sel == 29 and self.session.open(board29):
            pass
        if self.sel == 30 and self.session.open(board30):
            pass
        if self.sel == 31 and self.session.open(board31):
            pass
        if self.sel == 32 and self.session.open(board32):
            pass
        if self.sel == 33 and self.session.open(board33):
            pass
        if self.sel == 34 and self.session.open(board34):
            pass
        if self.sel == 35 and self.session.open(board35):
            pass
        if self.sel == 36 and self.session.open(board36):
            pass
        if self.sel == 37 and self.session.open(board37):
            pass
        if self.sel == 38 and self.session.open(board38):
            pass
        if self.sel == 39 and self.session.open(board39):
            pass
        if self.sel == 40 and self.session.open(board40):
            pass
        if self.sel == 41 and self.session.open(board41):
            pass
        if self.sel == 42 and self.session.open(board42):
            pass
        if self.sel == 43 and self.session.open(board43):
            pass
        if self.sel == 44 and self.session.open(board44):
            pass
        if self.sel == 45 and self.session.open(board45):
            pass
        if self.sel == 46 and self.session.open(board46):
            pass
        if self.sel == 47 and self.session.open(board47):
            pass
        if self.sel == 48 and self.session.open(board48):
            pass


    def update(self):
        if not fileExists('/tmp/file.txt'):
            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra; wget http://read.cba.pl/box/feed-panel/version.txt')
            self.chackupdate()
        else :
            self.KeyOk()

    def chackupdate(self):
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt'):
            self.session.open(MessageBox, _('Niepowodzenie aktualizacji.\nPrzepraszamy...  awaria serwera'), MessageBox.TYPE_INFO, 5)
        else:
            version = open('/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt', 'r')
            mypath = float(version.read().strip())
            version.close()
            if float(PLUGINVERSION) != mypath:
                message = _('Na serwerze jest do pobrania \nnowsza wersja Panel Extra Feeed . \nCzy chcesz aby dokonano aktualizacji wtyczki ?')
                ybox = self.session.openWithCallback(self.aktualizacjaef, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Aktualizacja wtyczki...'))
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt'):
                os.system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt; rm -f /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt.*; rm -f /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/wget-log')
                self.KeyOk()

    def aktualizacjaef(self, yesno):
        if yesno:
            if fileExists('/tmp/*.tar.gz'):
                os.system('rm /tmp/*.tar.gz')
            else:
                os.system('cd /tmp; wget http://read.cba.pl/box/feed-panel/update.tar.gz')
                if not fileExists('/tmp/update.tar.gz'):
                    self.session.open(MessageBox, _(' Nie znaleziono pliku dla aktualizacji.'), MessageBox.TYPE_INFO, 5)
                else:
                    os.system('rm -rf /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra; sleep 3')
                    os.system('tar -xzvf /tmp/update.tar.gz -C /')
                    restartbox = self.session.openWithCallback(self.restartE2, MessageBox, _('Aktualizacja wykonana. \nUruchamianie procesu restartu enigmy.. '), MessageBox.TYPE_INFO, 8)
        else:
            os.system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt; rm -f /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/version.txt.*; rm -f /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/wget-log')
            os.system('touch /tmp/file.txt')
            self.session.open(MessageBox, _('Aktualizacja anulowana.'), MessageBox.TYPE_INFO, 3)

    def restartE2(self, yesno):
        if yesno:
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/feedpanel.py'):
                os.system('rm /tmp/update.tar.gz')
                os.system('killall -9 enigma2')
            else:
                self.close()

    def updateLib(self):
        if fileExists('/lib/libcrypto.so.1.0.0'):
            os.system('rm -f /usr/lib/libcrypto.so.1.0.0')
            os.system('ln -s /lib/libcrypto.so.1.0.0 /usr/lib/libcrypto.so.1.0.0; ln -s /usr/lib/libssl.so.1.0.0 /usr/lib/libssl.so.1.0.2')
            os.system('ln -s /lib/libcrypto.so.1.0.0 /usr/lib/libcrypto.so.1.0.2; ln -s /lib/libcrypto.so.1.0.0 /usr/lib/libcrypto.so.0.9.8')
            os.system('ln -s /usr/lib/libssl.so.1.0.0 /usr/lib/libssl.so.0.9.8')
            self.updatePanel()

    def updatePanel(self):
        os.system('wget http://read.cba.pl/box/feed-panel/main.sh -O - | /bin/sh')
        self.updateList()

    def updatePlatform(self):
        if not fileExists('/etc/platform'):
            os.system('uname -m > /etc/platform')
            self.updateLib()

    def exitPlugin(self):
        if not fileExists('/tmp/install/plugin.txt'):
            os.system('rm -f /home/root/wget-log; rm -f /home/root/wget-log.*; rm -f /tmp/file.txt')
            self.close()
        else:
            os.system('rm -f /home/root/wget-log; rm -f /home/root/wget-log.*; rm -rf /tmp/install/; rm -f /tmp/wget-log*; rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh; rm -f /tmp/file.txt')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('System wymaga ponownego uruchomienia.\nCzy chcesz, aby wykonano Restart Gui?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Potwierdzenie wyboru ...'))

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()


class board0(Screen):
    skin = '\n<screen name="airly" position="center,center" size="760,570" flags="wfNoBorder" title="Airly">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/airly.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Airly'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/airly.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/airly.sh'
            system(cmd2)
            cmd3 = '/tmp/airly.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Airly/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board1(Screen):
    skin = '\n<screen name="bootstart" position="center,center" size="760,570" flags="wfNoBorder" title="Bootvideo">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,109" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz ... " position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Plugin Bootvideo'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Dodatkowe bootvideo.mp4'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(boot0):
            pass
        if self.sel == 1 and self.session.open(boot1):
            pass

class boot0(Screen):
    skin = '\n<screen name="bootvideo" position="center,center" size="760,570" flags="wfNoBorder" title="Plugin Bootvideo">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/bootvideo.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Plugin Bootvideo'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/bootVideo.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/bootVideo.sh'
            system(cmd2)
            cmd3 = '/tmp/bootVideo.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd6 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd7 = ('rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class boot1(Screen):
    skin = '\n<screen name="bootmp4" position="center,center" size="760,570" flags="wfNoBorder" title="Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,109" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz plik bootvideo.mp4 ... " position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     1'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     2'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     3'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     4'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     5'), png, 4)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     6'), png, 5)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wybierz bootvideo.mp4     7'), png, 6)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(bootanime0):
            pass
        if self.sel == 1 and self.session.open(bootanime1):
            pass
        if self.sel == 2 and self.session.open(bootanime2):
            pass
        if self.sel == 3 and self.session.open(bootanime3):
            pass
        if self.sel == 4 and self.session.open(bootanime4):
            pass
        if self.sel == 5 and self.session.open(bootanime5):
            pass
        if self.sel == 6 and self.session.open(bootanime6):
            pass

class bootanime0(Screen):
    skin = '\n<screen name="bootanime0" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota1.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class bootanime1(Screen):
    skin = '\n<screen name="bootanime1" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota2.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv2.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv2.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class bootanime2(Screen):
    skin = '\n<screen name="bootanime2" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota3.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv3.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv3.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class bootanime3(Screen):
    skin = '\n<screen name="bootanime3" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota4.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv4.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv4.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class bootanime4(Screen):
    skin = '\n<screen name="bootanime4" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota5.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv5.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv5.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class bootanime5(Screen):
    skin = '\n<screen name="bootanime5" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota6.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv6.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv6.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class bootanime6(Screen):
    skin = '\n<screen name="bootanime6" position="center,center" size="760,570" flags="wfNoBorder" title="Plik Bootvideo.mp4">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego pliku..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boota7.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj plik bootvideo.mp4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootvideo.mp4'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/bootvideo/bv7.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/bv7.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootvideo.mp4'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board2(Screen):
    skin = '\n<screen name="bootlogo" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,109" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz bootlogo" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 1'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 2'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 3'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 4'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 5'), png, 4)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 6'), png, 5)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 7'), png, 6)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 8'), png, 7)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 9'), png, 8)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 10'), png, 9)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 11'), png, 10)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 12'), png, 11)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 13'), png, 12)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 14'), png, 13)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 15'), png, 14)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 16'), png, 15)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 17'), png, 16)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 18'), png, 17)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 19'), png, 18)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 20'), png, 19)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 21'), png, 20)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 22'), png, 21)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 23'), png, 22)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 24'), png, 23)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 25'), png, 24)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 26'), png, 25)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 27'), png, 26)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Bootlogo 28'), png, 27)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(logo0):
            pass
        if self.sel == 1 and self.session.open(logo1):
            pass
        if self.sel == 2 and self.session.open(logo2):
            pass
        if self.sel == 3 and self.session.open(logo3):
            pass
        if self.sel == 4 and self.session.open(logo4):
            pass
        if self.sel == 5 and self.session.open(logo5):
            pass
        if self.sel == 6 and self.session.open(logo6):
            pass
        if self.sel == 7 and self.session.open(logo7):
            pass
        if self.sel == 8 and self.session.open(logo8):
            pass
        if self.sel == 9 and self.session.open(logo9):
            pass
        if self.sel == 10 and self.session.open(logo10):
            pass
        if self.sel == 11 and self.session.open(logo11):
            pass
        if self.sel == 12 and self.session.open(logo12):
            pass
        if self.sel == 13 and self.session.open(logo13):
            pass
        if self.sel == 14 and self.session.open(logo14):
            pass
        if self.sel == 15 and self.session.open(logo15):
            pass
        if self.sel == 16 and self.session.open(logo16):
            pass
        if self.sel == 17 and self.session.open(logo17):
            pass
        if self.sel == 18 and self.session.open(logo18):
            pass
        if self.sel == 19 and self.session.open(logo19):
            pass
        if self.sel == 20 and self.session.open(logo20):
            pass
        if self.sel == 21 and self.session.open(logo21):
            pass
        if self.sel == 22 and self.session.open(logo22):
            pass
        if self.sel == 23 and self.session.open(logo23):
            pass
        if self.sel == 24 and self.session.open(logo24):
            pass
        if self.sel == 25 and self.session.open(logo25):
            pass
        if self.sel == 26 and self.session.open(logo26):
            pass
        if self.sel == 27 and self.session.open(logo27):
            pass

class logo0(Screen):
    skin = '\n<screen name="boot0" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot1.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 1'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot1.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot1.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo1(Screen):
    skin = '\n<screen name="boot1" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot2.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 2'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot2.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot2.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo2(Screen):
    skin = '\n<screen name="boot2" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot3.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 3'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot3.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot3.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo3(Screen):
    skin = '\n<screen name="boot3" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot4.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot4.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot4.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo4(Screen):
    skin = '\n<screen name="boot4" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot5.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 5'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot5.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot5.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo5(Screen):
    skin = '\n<screen name="boot5" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot6.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 6'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot6.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot6.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo6(Screen):
    skin = '\n<screen name="boot6" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot7.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 7'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot7.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot7.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo7(Screen):
    skin = '\n<screen name="boot7" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot8.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 8'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot8.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot8.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo8(Screen):
    skin = '\n<screen name="boot8" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot9.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 9'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot9.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot9.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo9(Screen):
    skin = '\n<screen name="boot9" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot10.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 10'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot10.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot10.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo10(Screen):
    skin = '\n<screen name="boot10" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot11.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 11'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot11.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot11.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo11(Screen):
    skin = '\n<screen name="boot11" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot12.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 12'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot12.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot12.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo12(Screen):
    skin = '\n<screen name="boot12" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot13.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 13'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot13.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot13.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo13(Screen):
    skin = '\n<screen name="boot13" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot14.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 14'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot14.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot14.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo14(Screen):
    skin = '\n<screen name="boot14" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot15.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 15'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot15.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot15.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo15(Screen):
    skin = '\n<screen name="boot15" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot16.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 16'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot16.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot16.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo16(Screen):
    skin = '\n<screen name="boot16" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot17.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 17'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot17.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot17.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo17(Screen):
    skin = '\n<screen name="boot17" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot18.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 18'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot18.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot18.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo18(Screen):
    skin = '\n<screen name="boot18" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot19.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 19'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot19.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot19.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo19(Screen):
    skin = '\n<screen name="boot19" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot20.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 20'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot20.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot20.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo20(Screen):
    skin = '\n<screen name="boot20" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot21.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 21'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot21.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot21.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo21(Screen):
    skin = '\n<screen name="boot21" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot22.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 22'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot22.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot22.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo22(Screen):
    skin = '\n<screen name="boot22" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot23.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 23'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot23.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot23.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo23(Screen):
    skin = '\n<screen name="boot23" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot24.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 24'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot24.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot24.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo24(Screen):
    skin = '\n<screen name="boot24" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot25.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 25'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot25.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot25.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo25(Screen):
    skin = '\n<screen name="boot25" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot26.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 26'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot26.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot26.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo26(Screen):
    skin = '\n<screen name="boot26" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot27.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 27'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot27.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot27.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class logo27(Screen):
    skin = '\n<screen name="boot27" position="center,center" size="760,570" flags="wfNoBorder" title="Bootlogo 1">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego bootloga" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/boot28.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Bootlogo 28'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm -f /usr/share/bootlogo.mvi'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/bootlogos/boot28.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/boot28.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/usr/share/bootlogo.mvi'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            elif fileExists('/usr/share/enigma2/bootlogo_wait.mvi'):
                cmd4 = ('cp -f /usr/share/bootlogo.mvi /usr/share/enigma2/bootlogo_wait.mvi')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)					
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board3(Screen):
    skin = '\n<screen name="emu" position="center,center" size="760,570" flags="wfNoBorder" title="Wybierz ...">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz ..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Emu Manager'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Emulatory & SoftCam.Key'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(emu1):
            pass
        if self.sel == 1 and self.session.open(emu2):
            pass

class emu1(Screen):
    skin = '\n<screen name="emu_manager" position="center,center" size="760,570" flags="wfNoBorder" title="Emu Manager">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/alto.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Emu Manager'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm -f /tmp/*.sh; rm /tmp/*.tar.gz; mkdir /media/usb/config; mkdir /media/usb/camd; rm -rf /usr/lib/enigma2/python/Plugins/Extensions/EmuManager'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/emuManager.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/emuManager.sh'
            system(cmd2)
            cmd3 = '/tmp/emuManager.sh'
            system(cmd3)
            cmd4 = 'sleep 3; rm /tmp/*.tar.gz'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/EmuCamManager/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class emu2(Screen):
    skin = '\n<screen name="select_emu" position="center,center" size="760,570" flags="wfNoBorder" title="Emulatory">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz plik..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Binarki dla Emu Managera (arm)'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Binarki dla Emu Managera (mips)'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('CCcam  -||- -||- (arm)'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('CCcam  -||- -||- (mips)'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Binarki OSCam (patch)  Jej@n'), png, 4)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Binarka OSCam - ICAM   Kitte888'), png, 5)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Plik SoftCam.Key'), png, 6)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(emulator):
            pass
        if self.sel == 1 and self.session.open(emulator2):
            pass
        if self.sel == 2 and self.session.open(emulator3):
            pass
        if self.sel == 3 and self.session.open(emulator4):
            pass
        if self.sel == 4 and self.session.open(emulator5):
            pass
        if self.sel == 5 and self.session.open(emulator6):
            pass
        if self.sel == 6 and self.session.open(emulator7):
            pass

class emulator(Screen):
    skin = '\n<screen name="oscam_arm" position="center,center" size="760,570" flags="wfNoBorder" title="Binarki ARM">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Vu+ ,Octagon 4008, Zgemma H9S... (arm)" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/osc.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'armv7l' or mypath == 'aarch64':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Instalacja binarek OSCam, Ncam'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.sh; rm -f /media/usb/camd/.emu; rm -f /media/hdd/camd/.emu'
            system(cmd)
            cmd1 = 'rm /tmp/*.tar.gz; cd /tmp; wget http://read.cba.pl/box/cam/oscam-manager.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/oscam-manager.sh; /tmp/oscam-manager.sh'
            system(cmd2)
            if fileExists('/tmp/.emu'):
                cmd3 = ('rm -f /tmp/.emu; rm /tmp/*.tar.gz; rm -f /tmp/*.sh; rm -f /media/usb/camd/.emu; rm -f /media/hdd/camd/.emu')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                os.system('rm -f /tmp/*.sh; rm /tmp/*.tar.gz')
                self.close()

class emulator2(Screen):
    skin = '\n<screen name="binarki_mips" position="center,center" size="760,570" flags="wfNoBorder" title="Binarki MIPS">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Vu+ ,DM 500 HD/800 SE... (mips)" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/osc.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'mips':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Instalacja binarek OSCam, Ncam,'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.sh; rm -f /media/usb/camd/.emu; rm -f /media/hdd/camd/.emu'
            system(cmd)
            cmd1 = 'rm /tmp/*.tar.gz; cd /tmp; wget http://read.cba.pl/box/cam/oscam-manager.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/oscam-manager.sh; /tmp/oscam-manager.sh'
            system(cmd2)
            if fileExists('/media/usb/camd/.emu'):
                cmd3 = ('rm -f /tmp/.emu; rm /tmp/*.tar.gz; rm -f /tmp/*.sh; rm -f /media/usb/camd/.emu; rm -f /media/hdd/camd/.emu')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                os.system('rm -f /tmp/*.sh; rm /tmp/*.tar.gz')
                self.close()

class emulator3(Screen):
    skin = '\n<screen name="cccam_arm" position="center,center" size="760,570" flags="wfNoBorder" title="CCcam 2.3.2 ARM">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="CCcam dla Emu Managera" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ccc.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'armv7l' or mypath == 'aarch64':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj CCcam (arm)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; opkg update && opkg install libxcrypt-compat; rm -f /media/usb/camd/.emu'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/cam/CCcam4k.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/CCcam4k.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/media/usb/camd/.emu'):
                cmd3 = ('rm /tmp/*.tar.gz; rm -f /media/usb/camd/.emu')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class emulator4(Screen):
    skin = '\n<screen name="cccam_mips" position="center,center" size="760,570" flags="wfNoBorder" title="CCcam 2.3.2 MIPS">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="CCcam dla Emu Managera" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ccc.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'mips':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj CCcam (mips)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; opkg update && opkg install libxcrypt-compat; rm -f /media/usb/camd/.emu'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/cam/CCcam.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/CCcam.tar.gz -C /; sleep 3'
            system(cmd2)
            if fileExists('/media/usb/camd/.emu'):
                cmd3 = ('rm /tmp/*.tar.gz; rm -f /media/usb/camd/.emu')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class emulator5(Screen):
    skin = '\n<screen name="oscam-patch" position="center,center" size="760,570" flags="wfNoBorder" title="OSCam patch">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="OSCam (patch 1884,1813,0B01)" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/patch.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if not mypath == 'nbox':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj binarki OSCam (Jej@n)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm -f /tmp/.emu; rm /tmp/*.tar.gz; rm -f /tmp/*.sh; rm -f /media/usb/camd/.emu; rm -f /media/hdd/camd/.emu'
            system(cmd)
            if fileExists('/media/usb/camd'):
                cmd1 = ('cd /tmp; wget http://read.cba.pl/box/cam/oscam-bin/openusb.sh')
                system(cmd1)
                cmd2 = ('chmod 755 /tmp/openusb.sh')
                system(cmd2)
                cmd3 = ('/tmp/openusb.sh')
                system(cmd3)

            if fileExists('/media/hdd/camd'):
                cmd4 = ('cd /tmp; wget http://read.cba.pl/box/cam/oscam-bin/openhdd.sh')
                system(cmd4)
                cmd5 = ('chmod 755 /tmp/openhdd.sh')
                system(cmd5)
                cmd6 = ('/tmp/openhdd.sh')
                system(cmd6)

            if fileExists('/tmp/.emu'):
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                cmd7 = ('rm /tmp/*.tar.gz; rm -f /tmp/.emu; rm -f /tmp/*.sh; rm -f /tmp/wget-log; rm -f /media/usb/camd/wget-log')
                system(cmd7)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                os.system('rm -f /tmp/*.sh; rm /tmp/*.tar.gz; rm -f /tmp/wget-log; rm -f /media/usb/camd/wget-log')
                self.close()

class emulator6(Screen):
    skin = '\n<screen name="bin-emu" position="center,center" size="760,570" flags="wfNoBorder" title="Binarka Emu">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Zainstaluj plik binarny..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pat.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if not mypath == 'nbox':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Binarka OSCam - ICAM   Kitte888'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm -f /tmp/.emu; rm /tmp/*.tar.gz; rm -f /tmp/*.sh; rm -f /media/usb/camd/.emu; rm -f /media/hdd/camd/.emu'
            system(cmd)
            if fileExists('/media/usb/camd'):
                cmd1 = ('cd /tmp; wget http://read.cba.pl/box/cam/oscam-bin/icam.sh')
                system(cmd1)
                cmd2 = ('chmod 755 /tmp/icam.sh')
                system(cmd2)
                cmd3 = ('/tmp/icam.sh')
                system(cmd3)

            if fileExists('/media/hdd/camd'):
                cmd4 = ('cd /tmp; wget http://read.cba.pl/box/cam/oscam-bin/icam.sh')
                system(cmd4)
                cmd5 = ('chmod 755 /tmp/icam.sh')
                system(cmd5)
                cmd6 = ('/tmp/icam.sh')
                system(cmd6)

            if fileExists('/tmp/.emu'):
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                cmd7 = ('rm /tmp/*.tar.gz; rm -f /tmp/.emu; rm -f /tmp/*.sh; rm -f /tmp/wget-log; rm -f /media/usb/camd/wget-log')
                system(cmd7)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                os.system('rm -f /tmp/*.sh; rm /tmp/*.tar.gz; rm -f /tmp/wget-log; rm -f /media/usb/camd/wget-log')
                self.close()

class emulator7(Screen):
    skin = '\n<screen name="softcam" position="center,center" size="760,570" flags="wfNoBorder" title="SoftCam.Key">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Pobierz aktualny plik..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/cck.png" alphatest="blend" position="190,190" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if not mypath == 'nbox':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj SoftCam.Key'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm -f /media/usb/config/SoftCam.Key'
            system(cmd)
            cmd1 = 'cd /media/usb/config; wget http://read.cba.pl/box/cam/SoftCam.Key'
            system(cmd1)
            if fileExists('/media/usb/config/SoftCam.Key'):
                self.session.open(MessageBox, _('Proces instalacji pliku - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji pliku... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board4(Screen):
    skin = '\n<screen name="e2iplayer" position="center,center" size="760,570" flags="wfNoBorder" title="E2iPlayer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz wtyczki do instalacji" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj e2iplayer-deps'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj E2iPlayer'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Symlink dla exteplayer3'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Ikony dla E2iPlayera'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(iptv):
            pass
        if self.sel == 1 and self.session.open(iptv2):
            pass
        if self.sel == 2 and self.session.open(iptv3):
            pass
        if self.sel == 3 and self.session.open(iptv4):
            pass

class iptv(Screen):
    skin = '\n<screen name="e2iplayer-deps" position="center,center" size="760,570" flags="wfNoBorder" title="E2iPlayer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="E2iPlayer" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/deps.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/platform'):
            fileExists('/etc/platform')
            f = open('/etc/platform', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'armv7l' or mypath == 'aarch64':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj e2iplayer-deps'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/deps.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/deps.sh'
            system(cmd2)
            cmd3 = '/tmp/deps.sh; sleep 3'
            system(cmd3)
            if fileExists('/usr/bin/duk'):
                cmd4 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh; rm /tmp/*.ipk')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            if fileExists('/tmp/.defect'):
                cmd5 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh; rm /tmp/*.ipk')
                system(cmd5)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                if not fileExists('/usr/bin/duk'):    
                    cmd6 = ('rm -f /tmp/*.sh; rm /tmp/*.ipk')
                    system(cmd6)
                    self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                    self.close()

class iptv2(Screen):
    skin = '\n<screen name="e2iplayer" position="center,center" size="760,570" flags="wfNoBorder" title="E2iPlayer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="E2iPlayer" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/iptv-p.png" alphatest="blend" position="154,188" size="454,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj E2iPlayer'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/e2player.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/e2player.sh'
            system(cmd2)
            cmd3 = '/tmp/e2player.sh; sleep 3'
            system(cmd3)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/plugin.py'):
                cmd4 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh; rm /tmp/*.tar.gz')
                system(cmd4)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            if fileExists('/tmp/.defect'):
                cmd5 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh; rm /tmp/*.tar.gz')
                system(cmd5)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/plugin.py'):    
                    cmd6 = ('rm -f /tmp/*.sh; rm /tmp/*.tar.gz')
                    system(cmd6)
                    self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                    self.close()

class iptv3(Screen):
    skin = '\n<screen name="symlink" position="center,center" size="760,570" flags="wfNoBorder" title="E2iPlayer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="E2iPlayer" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/iptv-p.png" alphatest="blend" position="154,188" size="454,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wykonaj symlink dla exteplayer3'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'echo "config.plugins.iptvplayer.exteplayer3path=/usr/bin/exteplayer3" >> /etc/enigma2/settings; sleep 1; killall -9 enigma2'
            system(cmd)
            self.close()

class iptv4(Screen):
    skin = '\n<screen name="ikony_iptv" position="center,center" size="760,570" flags="wfNoBorder" title="Ikony E2iPlayer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja ikon dla E2iPlayera" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/kas.png" alphatest="blend" position="190,188" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Ikony od kastor777  (135x135)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/plugin/kastor.tar.gz'
            system(cmd1)
            cmd2 = 'tar -xzvf /tmp/kastor.tar.gz -C /'
            system(cmd2)
            if fileExists('/tmp/kastor.tar.gz'):
                cmd3 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm /tmp/*.tar.gz')
                system(cmd3)
                self.session.open(MessageBox, _('Proces instalacji ikon - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji ikon... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board5(Screen):
    skin = '\n<screen name="media_portal" position="center,center" size="760,570" flags="wfNoBorder" title="Wybierz wtyczki">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz wtyczki do instalacji" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj python-youtube-dl'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj MediaPortal'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj mpgz dla MediaPortal'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj skin dla MediaPortal'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(mp0):
            pass
        if self.sel == 1 and self.session.open(mp1):
            pass
        if self.sel == 2 and self.session.open(mp2):
            pass
        if self.sel == 3 and self.session.open(mp3):
            pass

class mp0(Screen):
    skin = '\n<screen name="py-dll" position="center,center" size="760,570" flags="wfNoBorder" title="MediaPortal">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/media.png" alphatest="blend" position="138,188" size="482,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('python-youtube-dl  (OpenPLi, VTi, Hyperion ...)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/you-dll.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/you-dll.sh'
            system(cmd2)
            cmd3 = '/tmp/you-dll.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/bin/youtube-dl'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd7 = ('rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class mp1(Screen):
    skin = '\n<screen name="media_portal" position="center,center" size="760,570" flags="wfNoBorder" title="MediaPortal">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/media.png" alphatest="blend" position="138,188" size="482,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj MediaPortal'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/mp.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/mp.sh'
            system(cmd2)
            cmd3 = '/tmp/mp.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd7 = ('rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class mp2(Screen):
    skin = '\n<screen name="mpgz" position="center,center" size="760,570" flags="wfNoBorder" title="mpgz dla MP">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/mediagz.png" alphatest="blend" position="138,188" size="482,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj dodatek mpgz'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/plugin/enigma2-plugin-extensions-mpgz_all.ipk'
            system(cmd1)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py'):
                cmd2 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; opkg install --force-overwrite --force-reinstall --force-downgrade /tmp/enigma2-plugin-extensions-mpgz_all.ipk')
                system(cmd2)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd3 = ('rm /tmp/*.ipk')
                system(cmd3)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class mp3(Screen):
    skin = '\n<screen name="skin_mp" position="center,center" size="760,570" flags="wfNoBorder" title="Skin dla MP">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Dodatkowy skin Full HD dla MediaPortal" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/skin.png" alphatest="blend" position="138,188" size="482,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj skin dla MediaPortal'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/plugin/enigma2-skin-mediaportal-weed-darkgrey-skin-fhd_all.ipk'
            system(cmd1)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py'):
                cmd2 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; opkg install --force-overwrite --force-reinstall --force-downgrade /tmp/enigma2-skin-mediaportal-weed-darkgrey-skin-fhd_all.ipk')
                system(cmd2)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd3 = ('rm /tmp/*.ipk')
                system(cmd3)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board6(Screen):
    skin = '\n<screen name="neo" position="center,center" size="760,570" flags="wfNoBorder" title="NeoBoot">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/neo.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj NeoBoota'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget --no-check-certificate  https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/iNB.sh'
            system(cmd2)
            cmd3 = '/tmp/iNB.sh'
            system(cmd3)
            if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/plugin.py'):
                cmd4 = ('rm -f /tmp/*.sh')
                system(cmd4)
                self.session.open(MessageBox, _('Niepowodzenie. \nNeoBoot nie jest zainstalowany !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board7(Screen):
    skin = '\n<screen name="freeplayer" position="center,center" size="760,570" flags="wfNoBorder" title="Free Player">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/free.png" alphatest="blend" position="150,188" size="458,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj AdvancedFree Player'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/free.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/free.sh'
            system(cmd2)
            cmd3 = '/tmp/free.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AdvancedFreePlayer/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board8(Screen):
    skin = '\n<screen name="freecccam" position="center,center" size="760,570" flags="wfNoBorder" title="Free CCcam">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/frec.png" alphatest="blend" position="138,188" size="482,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Free CCcam'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/freeCam.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/freeCam.sh'
            system(cmd2)
            cmd3 = '/tmp/freeCam.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/FreeCccam/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board9(Screen):
    skin = '\n<screen name="freeserver" position="center,center" size="760,570" flags="wfNoBorder" title="FreeServer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/porn.png" alphatest="blend" position="112,188" size="531,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj FreeServer'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/freeServ.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/freeServ.sh'
            system(cmd2)
            cmd3 = '/tmp/freeServ.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/FreeServer/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board10(Screen):
    skin = '\n<screen name="cfg" position="center,center" size="760,570" flags="wfNoBorder" title="Zoom">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/cfg.png" alphatest="blend" position="140,188" size="480,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zoom free server Downloader'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/cfg.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/cfg.sh'
            system(cmd2)
            cmd3 = '/tmp/cfg.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Zoom/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board11(Screen):
    skin = '\n<screen name="s4aUpdater" position="center,center" size="760,570" flags="wfNoBorder" title="s4aUpdater">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/myupd.png" alphatest="blend" position="216,188" size="331,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj s4aUpdater'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/s4a.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/s4a.sh'
            system(cmd2)
            cmd3 = '/tmp/s4a.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/s4aUpdater/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board12(Screen):
    skin = '\n<screen name="shoutcast" position="center,center" size="760,570" flags="wfNoBorder" title="SHOUTcast">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/sh.png" alphatest="blend" position="140,187" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj SHOUTcast'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/shout.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/shout.sh'
            system(cmd2)
            cmd3 = '/tmp/shout.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/SHOUTcast/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board13(Screen):
    skin = '\n<screen name="sgd" position="center,center" size="760,570" flags="wfNoBorder" title="SGD">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/sdg.png" alphatest="blend" position="140,188" size="480,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Image Downloader'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/img.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/img.sh'
            system(cmd2)
            cmd3 = '/tmp/img.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/ImageDownloader/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board14(Screen):
    skin = '\n<screen name="dreamosat" position="center,center" size="760,570" flags="wfNoBorder" title="Key Updater">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/au.png" alphatest="blend" position="190,188" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj DreamOSat keyUpdater'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/oskey.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/oskey.sh'
            system(cmd2)
            cmd3 = '/tmp/oskey.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DreamOSatkeyUpdater/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board15(Screen):
    skin = '\n<screen name="j00zek" position="center,center" size="760,570" flags="wfNoBorder" title="J00zek Bouquets">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/bj.png" alphatest="blend" position="140,188" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj J00zek Bouquets'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/dj.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/dj.sh'
            system(cmd2)
            cmd3 = '/tmp/dj.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/J00zekBouquets/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board16(Screen):
    skin = '\n<screen name="m3uPlayer" position="center,center" size="760,570" flags="wfNoBorder" title="m3uPlayer">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/m3u.png" alphatest="blend" position="140,188" size="472,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj m3uPlayer'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/m3u.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/m3u.sh'
            system(cmd2)
            cmd3 = '/tmp/m3u.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/m3uPlayer/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board17(Screen):
    skin = '\n<screen name="userskin" position="center,center" size="760,570" flags="wfNoBorder" title="UserSkin Setup">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/user.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj UserSkin Setup'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/user.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/user.sh'
            system(cmd2)
            cmd3 = '/tmp/user.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/UserSkin/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board18(Screen):
    skin = '\n<screen name="select_skin" position="center,center" size="760,570" flags="wfNoBorder" title="Wybierz skin">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz skin ..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Full HD Glass'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('BLACK ALL FHD'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Black FHD - mod C7 (VTi)'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Burgund FHD  (VTi)'), png, 3)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Pingu Dark-Blue FHD  (BH)'), png, 4)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('PLi-FullNightHD Mod-Mercus (OpenATV)'), png, 5)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('Noia FHD (OpenPLi)'), png, 6)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
#        res = (_('NoName'), png, 7)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
#        png = LoadPixmap(mypixmap)
#        res = (_('NoName'), png, 8)
#        self.list.append(res)
#        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
#        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(skin):
            pass
        if self.sel == 1 and self.session.open(skin2):
            pass
        if self.sel == 2 and self.session.open(skin3):
            pass
        if self.sel == 3 and self.session.open(skin4):
            pass
        if self.sel == 4 and self.session.open(skin5):
            pass
        if self.sel == 5 and self.session.open(skin6):
            pass
        if self.sel == 6 and self.session.open(skin7):
            pass
        if self.sel == 7 and self.session.open(skin8):
            pass
        if self.sel == 8 and self.session.open(skin9):
            pass

class skin(Screen):
    skin = '\n<screen name="skin_glass" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranego skina" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/glass.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Full HD Glass'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin.sh'
            system(cmd2)
            cmd3 = '/tmp/skin.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class skin2(Screen):
    skin = '\n<screen name="skin_blackall" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Skin dla image open..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/bfhd.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj BLACK ALL FHD'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin2.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin2.sh'
            system(cmd2)
            cmd3 = '/tmp/skin2.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/enigma2/BLACK_ALL_FHD/skin.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class skin3(Screen):
    skin = '\n<screen name="blackallc7" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Skin dla image VTi" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/fhdc7.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Black FHD - mod C7'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin3.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin3.sh'
            system(cmd2)
            cmd3 = '/tmp/skin3.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/enigma2/BLACK_FHD_VTI_modC7/skin.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class skin4(Screen):
    skin = '\n<screen name="skin_burgund" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Skin dla image VTi" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/burgund.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Burgund FHD'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin4.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin4.sh'
            system(cmd2)
            cmd3 = '/tmp/skin4.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/enigma2/BURGUND_FHD_VTI/skin.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class skin5(Screen):
    skin = '\n<screen name="skin_pingu" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Skin dla image Black Hole" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pingu.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Pingu Dark-Blue FHD'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin5.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin5.sh'
            system(cmd2)
            cmd3 = '/tmp/skin5.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/enigma2/Pingu-DarkBlue/skin.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class skin6(Screen):
    skin = '\n<screen name="pli-night" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Skin dla image OpenATV..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/night.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj PLi-FullNightHD (OpenATV)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin6.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin6.sh'
            system(cmd2)
            cmd3 = '/tmp/skin6.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/enigma2/PLi-FullNightHD-Mod-M/skin.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class skin7(Screen):
    skin = '\n<screen name="skin_noia" position="center,center" size="760,570" flags="wfNoBorder" title="Instalacja skina">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Skin dla image OpenPLi" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/nfhd.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Noia FHD'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/skin7.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/skin7.sh'
            system(cmd2)
            cmd3 = '/tmp/skin7.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/share/enigma2/Noia_FHD/skin.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji skina - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board19(Screen):
    skin = '\n<screen name="lcd" position="center,center" size="760,570" flags="wfNoBorder" title="Lcd4linux">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/air.png" alphatest="blend" position="190,188" size="380,270" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Lcd4linux'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/lcd.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/lcd.sh'
            system(cmd2)
            cmd3 = '/tmp/lcd.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/LCD4linux/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board20(Screen):
    skin = '\n<screen name="picons" position="center,center" size="760,570" flags="wfNoBorder" title="Update picons">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="2" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pic.png" alphatest="blend" position="138,188" size="482,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Chocholousek picons'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/pic.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/pic.sh'
            system(cmd2)
            cmd3 = '/tmp/pic.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/ChocholousekPicons/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board24(Screen):
    skin = '\n<screen name="extnumzap" position="center,center" size="760,570" flags="wfNoBorder" title="ExtNumberZap">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/numzap.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj ExtNumberZap'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/zap.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/zap.sh'
            system(cmd2)
            cmd3 = '/tmp/zap.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/NumberZapExt/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board25(Screen):
    skin = '\n<screen name="menusort" position="center,center" size="760,570" flags="wfNoBorder" title="MenuSort">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/men.png" alphatest="blend" position="190,188" size="380,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj MenuSort'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/sort.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/sort.sh'
            system(cmd2)
            cmd3 = '/tmp/sort.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MenuSort/keymap.xml'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board26(Screen):
    skin = '\n<screen name="pluginsort" position="center,center" size="760,570" flags="wfNoBorder" title="PluginSort">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/serv.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj PluginSort'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/psort.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/psort.sh'
            system(cmd2)
            cmd3 = '/tmp/psort.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/pluginsort/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board27(Screen):
    skin = '\n<screen name="signal" position="center,center" size="760,570" flags="wfNoBorder" title="Quick Signal">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki ..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/signal.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj RaedQuickSignal'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/raed.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/raed.sh'
            system(cmd2)
            cmd3 = '/tmp/raed.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/RaedQuickSignal/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd6 = ('rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board28(Screen):
    skin = '\n<screen name="ajpanel" position="center,center" size="760,570" flags="wfNoBorder" title="AJPanel">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/gold.png" alphatest="blend" position="116,180" size="531,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj  AJPanel'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/gold.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/gold.sh'
            system(cmd2)
            cmd3 = '/tmp/gold.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AJPan/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board29(Screen):
    skin = '\n<screen name="dreamsat" position="center,center" size="760,570" flags="wfNoBorder" title="DreamSat Panel">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/dreamsat.png" alphatest="blend" position="215,188" size="325,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj DreamSat Panel'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/dreamsat.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/dreamsat.sh'
            system(cmd2)
            cmd3 = '/tmp/dreamsat.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/plugin.py') or ('/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/plugin.pyc'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board30(Screen):
    skin = '\n<screen name="levi45-addon" position="center,center" size="760,570" flags="wfNoBorder" title="Levi45 Panel">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/iw2.png" alphatest="blend" position="186,185" size="391,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Levi45 Addon Manager'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/levi45-addon.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/levi45-addon.sh'
            system(cmd2)
            cmd3 = '/tmp/levi45-addon.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Levi45Addons/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board32(Screen):
    skin = '\n<screen name="satvenus" position="center,center" size="760,570" flags="wfNoBorder" title="SatVenus">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/venus.png" alphatest="blend" position="216,188" size="331,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj SatVenus Panel Addons'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/satven.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/satven.sh'
            system(cmd2)
            cmd3 = '/tmp/satven.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/SatVenusPanel/plugin.pyo'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board33(Screen):
    skin = '\n<screen name="historyzap" position="center,center" size="760,570" flags="wfNoBorder" title="HistoryZap">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="435,513" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Wtyczka dla image OpenPLi" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/his.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj HistoryZapSelector'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/his.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/his.sh'
            system(cmd2)
            cmd3 = '/tmp/his.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect2'):
                cmd6 = ('rm -f /tmp/.defect2; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nBrak wsparcia dla twojego image !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board34(Screen):
    skin = '\n<screen name="netspeedtest" position="center,center" size="760,570" flags="wfNoBorder" title="Internet SpeedTest">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/netspeed.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Internet SpeedTest'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/inter.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/inter.sh'
            system(cmd2)
            cmd3 = '/tmp/inter.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/InternetSpeedTest/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board35(Screen):
    skin = '\n<screen name="ciplus" position="center,center" size="760,570" flags="wfNoBorder" title="Wybierz...">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,353" backgroundColor="#00000000" foregroundColor="#00cc9966" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/pod.png" backgroundColorSelected="#00000000" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/exit.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ok.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <eLabel text="Wybierz CI+ dla image ..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="135,513" alphatest="blend" size="30,30" zPosition="3" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateList(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('CI+ Install dla OpenPLi  7.2 & 7.3 & 8.0'), png, 0)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('CI+ Helper dla OpenPLi  8.1'), png, 1)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        res = (_('CI+ Helper dla openATV  6.2 & 6.3 & 6.4'), png, 2)
        self.list.append(res)
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb2.png'
        png = LoadPixmap(mypixmap)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(ciplus1):
            pass
        if self.sel == 1 and self.session.open(ciplus2):
            pass
        if self.sel == 2 and self.session.open(ciplus3):
            pass

class ciplus1(Screen):
    skin = '\n<screen name="ciplus1" position="center,center" size="760,570" flags="wfNoBorder" title="CI+">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="41,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ci+.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/issue.net'):
            fileExists('/etc/issue.net')
            f = open('/etc/issue.net', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'openpli 7.2-release %h' or mypath == 'openpli 7.3-release %h' or mypath == 'openpli 8.0-release %h':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj CI+ dla OpenPLi  7.2 & 7.3 & 8.0'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.ipk; opkg remove enigma2-plugin-ciplusinstall --force-overwrite; opkg remove enigma2-plugin-systemplugins-ciplusinstall --force-overwrite'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/plugin/enigma2-plugin-systemplugins-ciplusinstall_1.8_all.ipk'
            system(cmd1)
            cmd2 = 'opkg install --force-overwrite /tmp/*.ipk'
            system(cmd2)
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('Uruchamianie procesu restartu enigmy.. '), MessageBox.TYPE_INFO, 6)

    def restartGUI(self, yesno):
        if yesno:
            if fileExists('/usr/bin/enigma2'):
                os.system('rm /tmp/*.ipk')
                os.system('killall -9 enigma2')
            else:
                self.close()

class ciplus2(Screen):
    skin = '\n<screen name="ciplus2" position="center,center" size="760,570" flags="wfNoBorder" title="CI+">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="41,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ci+.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/issue.net'):
            fileExists('/etc/issue.net')
            f = open('/etc/issue.net', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'openpli 8.1-release %h':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj CI+ Helper dla OpenPLi  8.1'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.ipk; opkg remove enigma2-plugin-ciplusinstall --force-overwrite; opkg remove enigma2-plugin-systemplugins-ciplusinstall --force-overwrite'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/plugin/enigma2-plugin-extensions-ci_plus_helper-openpli8_all.ipk'
            system(cmd1)
            cmd2 = 'opkg install --force-overwrite /tmp/*.ipk'
            system(cmd2)
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('Uruchamianie procesu restartu enigmy.. '), MessageBox.TYPE_INFO, 6)

    def restartGUI(self, yesno):
        if yesno:
            if fileExists('/usr/bin/enigma2'):
                os.system('rm /tmp/*.ipk')
                os.system('killall -9 enigma2')
            else:
                self.close()

class ciplus3(Screen):
    skin = '\n<screen name="ciplus3" position="center,center" size="760,570" flags="wfNoBorder" title="CI+">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="41,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki..." position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ci+.png" alphatest="blend" position="191,188" size="384,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateInfo()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def updateInfo(self):
        if fileExists('/etc/issue.net'):
            fileExists('/etc/issue.net')
            f = open('/etc/issue.net', 'r')
        mypath = f.readline().strip()
        f.close()
        if mypath == 'Welcome to openATV for %h':
            self.downList()
        else:
            self.close()

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('CI+ dla openATV 6.2 & 6.3 & 6.4'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.ipk'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/plugin/enigma2-plugin-systemplugins-ciplushelper_4.7-r0_all.ipk'
            system(cmd1)
            cmd2 = 'opkg install --force-overwrite /tmp/*.ipk'
            system(cmd2)
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('Uruchamianie procesu restartu enigmy.. '), MessageBox.TYPE_INFO, 6)

    def restartGUI(self, yesno):
        if yesno:
            if fileExists('/usr/bin/enigma2'):
                os.system('rm /tmp/*.ipk')
                os.system('killall -9 enigma2')
            else:
                self.close()

class board37(Screen):
    skin = '\n<screen name="nst" position="center,center" size="760,570" flags="wfNoBorder" title="Ncam Status">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ncstat.png" alphatest="blend" position="140,188" size="479,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Ncam Status'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/nst.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/nst.sh'
            system(cmd2)
            cmd3 = '/tmp/nst.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NcamStatus/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board38(Screen):
    skin = '\n<screen name="ost" position="center,center" size="760,570" flags="wfNoBorder" title="Oscam Status">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oscst.png" alphatest="blend" position="191,188" size="364,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Oscam Status'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/ost.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/ost.sh'
            system(cmd2)
            cmd3 = '/tmp/ost.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/OscamStatus/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board39(Screen):
    skin = '\n<screen name="clock" position="center,center" size="760,570" flags="wfNoBorder" title="Permanentclock">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/zegar.png" alphatest="blend" position="198,188" size="364,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj Permanentclock'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/zegar.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/zegar.sh'
            system(cmd2)
            cmd3 = '/tmp/zegar.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/BundesligaPermanentClock/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board40(Screen):
    skin = '\n<screen name="weather" position="center,center" size="760,570" flags="wfNoBorder" title="TheWeather">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/weather.png" alphatest="blend" position="198,188" size="364,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj TheWeather'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/weather.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/weather.sh'
            system(cmd2)
            cmd3 = '/tmp/weather.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/TheWeather/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()

class board41(Screen):
    skin = '\n<screen name="youtube" position="center,center" size="760,570" flags="wfNoBorder" title="YouTube">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/board1.png" position="0,0" size="760,570" zPosition="-2" />\n    <widget source="list" render="Listbox" position="40,110" size="680,60" backgroundColorSelected="#00191919" foregroundColorSelected="#0009f4f6" zPosition="2" scrollbarMode="showNever" transparent="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/36.png">\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (65, 1), size = (600, 50), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n    MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (50, 50), png = 1),\n  ],\n  "fonts": [gFont("Regular", 28)],\n    "itemHeight": 50\n    } \n    </convert>\n    </widget>\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/ex.png" alphatest="blend" position="170,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/red.png" position="132,510" alphatest="blend" size="30,30" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/oki.png" alphatest="blend" position="470,499" size="140,50" zPosition="3" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/green.png" position="432,510" alphatest="blend" size="30,30" zPosition="3" />\n    <eLabel text="Instalacja wybranej wtyczki" position="30,27" size="700,36" halign="center" valign="center" foregroundColor="#00ff6600" transparent="1" zPosition="3" font="Regular; 30" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/ikon/yt.png" alphatest="blend" position="198,188" size="364,271" zPosition="5" />\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'red': self.close,
         'green': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/mb.png'
        png = LoadPixmap(mypixmap)
        res = (_('Zainstaluj YouTube (mod by Taapat)'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk; rm -f /tmp/*.sh'
            system(cmd)
            cmd1 = 'cd /tmp; wget http://read.cba.pl/box/skrypt/yt.sh'
            system(cmd1)
            cmd2 = 'chmod -R +x /tmp/yt.sh'
            system(cmd2)
            cmd3 = '/tmp/yt.sh'
            system(cmd3)
            cmd4 = 'rm /tmp/*.tar.gz; rm /tmp/*.ipk'
            system(cmd4)
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/YouTube/plugin.py'):
                cmd5 = ('mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -f /tmp/*.sh')
                system(cmd5)
                self.session.open(MessageBox, _('Proces instalacji wtyczki - wykonany poprawnie !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.defect'):
                cmd6 = ('rm -f /tmp/.defect; rm -f /tmp/*.sh')
                system(cmd6)
                self.session.open(MessageBox, _('Niepowodzenie. \nWersja pythona jest niezgodna !'), MessageBox.TYPE_INFO, 5)
                self.close()
            elif fileExists('/tmp/.fault'):
                cmd7 = ('rm -f /tmp/.fault; rm -f /tmp/*.sh')
                system(cmd7)
                self.session.open(MessageBox, _('Sorry. Pobranie wtyczki \nchwilowo jest zablokowane!'), MessageBox.TYPE_INFO, 5)
                self.close()
            else:
                cmd8 = ('rm -f /tmp/*.sh')
                system(cmd8)
                self.session.open(MessageBox, _('Niepowodzenie. \nZatrzymano proces instalacji... !'), MessageBox.TYPE_INFO, 5)
                self.close()