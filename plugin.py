# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra/plugin.py
from Plugins.Plugin import PluginDescriptor
from .feedpanel import mainboard

def main(session, **kwargs):
    session.open(mainboard)

def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('Panel Extra Feed'),
          main,
          'panel_extra_feed',
          1)]
    return []

def Plugins(**kwargs):
    list = [PluginDescriptor(name='Panel Extra Feed', description=_('Pobierz i zainstaluj dodatkowe wtyczki...'), icon='plugin.png', where=[PluginDescriptor.WHERE_MENU], fnc=menu), PluginDescriptor(name='Panel Extra Feed', description=_('Dodatkowe wtyczki do instalacji...'), icon='plugin.png', where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=main)]
    return list