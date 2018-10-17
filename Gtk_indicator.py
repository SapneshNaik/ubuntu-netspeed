import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


class Appindicator:

    INDICATOR_LABEL_GUIDE = "00:00"

    DEFAULT_LABEL = "\u2193"+ b" 0.0 KiB/s ".decode("utf-8") + "\u2191" + b"0.0 KiB/s".decode("utf-8")

    def __init__(self, root):
        self.app = root
        self.indicator = appindicator.Indicator.new(
                    self.app.name,
                    "",
                    appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_label(self.DEFAULT_LABEL, self.INDICATOR_LABEL_GUIDE )
    
        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Settings")
        self.menu.append(item)

        #Sub menu Not working.
        #submenu for different units
        self.sub_menu = Gtk.Menu()
        submenu_item = Gtk.MenuItem()
        submenu_item.set_label("Units")
        self.sub_menu.append(submenu_item)
        item.set_submenu(self.sub_menu)



        item = Gtk.MenuItem()
        item.set_label("Interfaces")
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
