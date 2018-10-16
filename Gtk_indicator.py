import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


class Appindicator:
    def __init__(self, root):
        self.app = root
        self.indicator = appindicator.Indicator.new(
                    self.app.name,
                    "",
                    appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_label("Sapnesh Naik", "80% thrust")
    
        self.menu = Gtk.Menu()
        item = Gtk.MenuItem()
        item.set_label("Main Window")
        item.connect("activate", self.app.main_window.cb_show, '')
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Configuration")
        item.connect("activate", self.app.config_window.cb_show, '')
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.cb_exit, '')
        self.menu.append(item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

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
