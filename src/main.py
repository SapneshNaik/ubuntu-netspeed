#!/usr/bin/python3

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

    UPLOAD_SYMBOL = "\u2191" #unicode Up Arrow symbol
    DOWNLOAD_SYMBOL = "\u2193" #unicode Down Arrow symbol
    INDICATOR_LABEL_GUIDE = "00:00"
    BYTE_THRESHHOLD = False #determine if Ux, Tx value below 1024 bytes should be ignored or not 

    def __init__(self, app_name):
        self.name = app_name
        self.main_window = AppMainWindow(self)
        self.config_window = AppConfigWindow(self)
        self.indicator = Appindicator(self)

    def run(self):

        ''' 
            This function calculates the Tx (Download) and Ux (Upload) bytes every 2 seconds. The application listens on the default 
            interface by default.
            Logic: 
               1 - get the Tx and Ux Bytes and the current timestamp [Tx1, Ux1, t1].
               2 - sleep for n seconds.
               3 - get the Tx and Ux Bytes again and the current timestamp [Tx2, Ux2, t2].
               4 - Calculate the network speed using the formula:
                    TxSpeed = (Tx2-Tx1)/ (t2-t1)
                    UxSpeed = (Ux2-Ux1)/ (t2-t1)
        '''
        
        def calculate_net_speed(rate, indicator, dt = 2, interface = Interfaces.get_default()):
            t0 = time.time()

            #loop untill we have a default (enabled) interface
            while interface is None:
                interface = Interfaces.get_default()

            counter = psutil.net_io_counters(pernic=True)[interface]
            tot = (counter.bytes_sent, counter.bytes_recv)

            while True:
                last_tot = tot
                time.sleep(dt)

                #cover an edge case, loop untill we have a default (enabled) interface
                while interface is None:
                    interface = Interfaces.get_default()

                counter = psutil.net_io_counters(pernic=True)[interface]
                t1 = time.time()
                tot = (counter.bytes_sent, counter.bytes_recv)
                ul, dl = [(now - last) / (t1 - t0)
                            for now, last in zip(tot, last_tot)]

                rate.append((ul, dl))
                update_speed(indicator)
                t0 = time.time()



        ''' 
            Automatically format the Tx and Ux bytes to approptiate Unit.
            We also ignore bytes below 1024 to prevent unnecessory UI updates 
        '''
        def auto_units(num):
            for unit in ['B/s','KiB/s','MiB/s','GiB/s','TiB/s','PiB/s','EiB/s','ZiB/s']:
                if (abs(num) < 1024.0):
                    if unit != 'B/s' and not self.BYTE_THRESHHOLD: 
                        return "%3.1f %s" % (num, unit)
                    else:
                        return "0.0 KiB/s" 

                num /= 1024.0
            return "%.1f %s" % (num, 'Yi')


        ''' 
            Update the indicator text with the current Upload and Doownload Speed.
            This method constructs the dl,ul speed string and writes it to the app indicator label.
        '''
        def update_speed(indicator):
                download_speed = auto_units(transfer_rate[0][1])
                upload_speed = auto_units(transfer_rate[0][0])
                label = self.DOWNLOAD_SYMBOL + download_speed + " " + self.UPLOAD_SYMBOL + upload_speed

                indicator.indicator.set_label( label, self.INDICATOR_LABEL_GUIDE)



        # deque of length 1 to hold the ul/dl- values
        transfer_rate = deque(maxlen=1)

        # Create a new thread for the network speed calculation which avoilds too much work on the main thread
        worker_thread = threading.Thread(target=calculate_net_speed, args=(transfer_rate, self.indicator))

        # # The program will exit if there are only daemonic threads left.
        worker_thread.daemon = True
        worker_thread.start()

        #Gracefully handle [CTRL+C] interrupt
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, quit)

        Gtk.main()



    def quit():
        Gtk.main_quit()

if __name__ == '__main__':
    app = UbuntuNetSpeed('ubuntu-netspeed')
    app.run()
