#!/usr/bin/python

from collections import deque
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from gi.repository import GLib
import psutil
import threading
import time
import signal

from Gtk_indicator import Appindicator
from Gtk_indicator import AppConfigWindow
from Gtk_indicator import AppMainWindow
from interfaces import Interfaces

class UbuntuNetSpeed(Gtk.Application):

    UPLOAD_SYMBOL = "\u2191"
    DOWNLOAD_SYMBOL = "\u2193"
    INDICATOR_LABEL_GUIDE = "00:00"
    BYTE_THRESHHOLD = False

    def __init__(self, app_name):
        self.name = app_name
        self.main_window = AppMainWindow(self)
        self.config_window = AppConfigWindow(self)
        self.indicator = Appindicator(self)


    def run(self):

        def calculate_net_speed(rate, indicator, dt = 2, interface = Interfaces.get_default()):
            t0 = time.time()
            counter = psutil.net_io_counters(pernic=True)[interface]
            tot = (counter.bytes_sent, counter.bytes_recv)

            while True:
                last_tot = tot
                time.sleep(dt)
                counter = psutil.net_io_counters(pernic=True)[interface]
                t1 = time.time()
                tot = (counter.bytes_sent, counter.bytes_recv)
                ul, dl = [(now - last) / (t1 - t0)
                          for now, last in zip(tot, last_tot)]

                rate.append((ul, dl))
                # print(auto_units(dl))
                update_speed(indicator)
                t0 = time.time()



        def auto_units(num):
            for unit in ['B/s','KiB/s','MiB/s','GiB/s','TiB/s','PiB/s','EiB/s','ZiB/s']:
                if (abs(num) < 1024.0):
                    if unit != 'B/s' and not self.BYTE_THRESHHOLD: 
                        return "%3.1f %s" % (num, unit)
                    else:
                        return "0.0 B/s" 

                num /= 1024.0
            return "%.1f %s" % (num, 'Yi')

        def update_speed(indicator):
                download_speed = auto_units(transfer_rate[0][1])
                upload_speed = auto_units(transfer_rate[0][0])
                label = self.UPLOAD_SYMBOL + upload_speed + " " + self.DOWNLOAD_SYMBOL + download_speed
                indicator.indicator.set_label( label, self.INDICATOR_LABEL_GUIDE)


        # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
        transfer_rate = deque(maxlen=1)

        worker_thread = threading.Thread(target=calculate_net_speed, args=(transfer_rate, self.indicator))

        # # The program will exit if there are only daemonic threads left.
        worker_thread.daemon = True
        worker_thread.start()
        #Gracefully handle CTRL+C interrupt
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, quit)
        # GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTSTP, quit)

        Gtk.main()



    def quit():
        Gtk.main_quit()

if __name__ == '__main__':
    app = UbuntuNetSpeed('ubuntu-netspeed')
    app.run()
