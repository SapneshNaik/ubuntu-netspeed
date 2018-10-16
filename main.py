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

class UbuntuNetSpeed(Gtk.Application):
    def __init__(self, app_name):
        self.name = app_name
        self.main_window = AppMainWindow(self)
        self.config_window = AppConfigWindow(self)
        self.indicator = Appindicator(self)


    def run(self):

        #TO-DO: Provide support for dynamic interface change 
        def calculate_net_speed(rate, indicator, dt=1, interface='enp3s0'):
            t0 = time.time()
            counter = psutil.net_io_counters(pernic=True)[interface]
            tot = (counter.bytes_sent, counter.bytes_recv)

            while True:
                last_tot = tot
                time.sleep(dt)
                counter = psutil.net_io_counters(pernic=True)[interface]
                t1 = time.time()
                tot = (counter.bytes_sent, counter.bytes_recv)
                ul, dl = [(now - last) / (t1 - t0) / 1000.0
                          for now, last in zip(tot, last_tot)]
                # print(ul, dl)
                rate.append((ul, dl))
                indicator.indicator.set_label("UL: {0:.0f} kB/s | DL: {1:.0f} kB/s".format(*transfer_rate[-1]), "80% thrust")
                t0 = time.time()


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
    app = MyApp('ubuntu-netspeed')
    app.run()
