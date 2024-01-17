"""
Custom Python driver for HUION H610 Pro v2

(C) James Adair 2024, All Rights Reserved
"""

import evdev
from evdev import InputDevice, ecodes
import time
from threading import Thread
from .errors import TabletDisconnected

XMAX = 50800
YMAX = 31750
PMAX = 8200

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480


def driver(tablet):
    while tablet.open:
        try:
            for event in tablet.device.read():
                if event.type == ecodes.EV_ABS:
                    # Process touchscreen events here
                    if event.code == ecodes.ABS_X:
                        tablet.x = 800*(event.value/XMAX)
                    elif event.code == ecodes.ABS_Y:
                        tablet.y = 480*(event.value/YMAX)

                    if event.code == ecodes.ABS_PRESSURE:
                        tablet.p = event.value/PMAX
                        # print(f"X: {x_position}, Y: {y_position}")
                        # print("Translated data:", 800*(y_position/YMAX), 480*(x_position/XMAX))
        except BlockingIOError:
            pass

class Tablet:
    def __init__(self, tablet_device):
        # Define variables to store touch event data
        self.x = 0
        self.y = 0
        self.p = 0  # pressure
        self.device = tablet_device
        self.file = open(self.device.path, 'rb')
        self.open = True
    
    def start_driver(self):
        self.open = True
        t = Thread(target=driver, args=(self,))
        t.start()

    def stop_driver(self):
        self.open = False  # Kill thread
        self.file.close()

    def get_pen_data(self):
        return (self.x, self.y, self.p)

# Find your tablet device
def find_device():
    print(evdev.list_devices())
    devices = [InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices: print(device.name, "on", device.path)
    tablet_device = None
    for device in devices:
        if "event" in device.path and "huion tablet pen" in device.name.lower():
            tablet_device = device
            break

    print()

    if tablet_device is None:
        print("Tablet device not found.")
        return None

    print(f"Using tablet device: {tablet_device.name} on {tablet_device.path}")
    return Tablet(tablet_device)

if __name__ == "__main__":
    try:
        tablet = find_device()
        if tablet:
            tablet.start_driver()
        else:
            raise TabletDisconnected()
        while True:
            time.sleep(0.1)
            data = tablet.get_pen_data()
            print(f"X: {data[0]}, Y: {data[1]}, Pressure: {data[2]}")
    except KeyboardInterrupt:
        tablet.stop_driver()