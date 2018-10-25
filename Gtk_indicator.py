''' This module defines the idicator for the application and initates the
    application's menus.
'''

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from interfaces import Interfaces

class Appindicator:

    INDICATOR_LABEL_GUIDE = "00:00"

    #The app takes approximately 2 seconds to start displaying the network speed. Until then show a default string
    DEFAULT_LABEL = "\u2193"+ b" 0.0 KiB/s ".decode("utf-8") + "\u2191" + b"0.0 KiB/s".decode("utf-8")

    def __init__(self, root):
        self.app = root
        self.indicator = appindicator.Indicator.new(
                    self.app.name,
                    "",
                    appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_label(self.DEFAULT_LABEL, self.INDICATOR_LABEL_GUIDE )
    
        self.main_menu = Gtk.Menu()

        main_menu_item = Gtk.MenuItem()
        main_menu_item.set_label("Settings")
        self.main_menu.append(main_menu_item)

        #settings sub menu
        settings_submenu = Gtk.Menu()

        interfaces = Gtk.MenuItem()
        interfaces.set_label("Interfaces")
        settings_submenu.append(interfaces)

  

        available_interfaces = Interfaces.get_interfaces()

        interfaces_submenu = Gtk.Menu()
        
        for i in available_interfaces:
            if i not in "lo":
                interfaces_submenu_item = Gtk.MenuItem()
                interfaces_submenu_item.set_label(i)
                interfaces_submenu.append(interfaces_submenu_item)

        interfaces.set_submenu(interfaces_submenu)

        settings_submenu_item = Gtk.MenuItem()
        settings_submenu_item.set_label("Units")
        settings_submenu.append(settings_submenu_item)

        main_menu_item.set_submenu(settings_submenu)


        main_menu_item = Gtk.MenuItem()
        main_menu_item.set_label("Exit")
        main_menu_item.connect("activate", self.cb_exit, '')
        self.main_menu.append(main_menu_item)

        #show menu items
        self.main_menu.show_all()

        #set menu to indicator
        self.indicator.set_menu(self.main_menu)

    def cb_exit(self, w, data):
        Gtk.main_quit()


class AppConfigWindow(Gtk.Window):
    def __init__(self, root):
        super().__init__()
        self.app = root
        self.set_title(self.app.name + ' Config Window')
  
    def cb_show(self, w, data):
        self.show()

class AppMainWindow(Gtk.Window):
    def __init__(self, root):
        super().__init__()
        self.app = root
        self.set_title(self.app.name)

    def cb_show(self, w, data):
        self.show()
