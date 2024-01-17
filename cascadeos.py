"""

CascadeOS
---
An operating system written in Python to control the CascadeTab 1.0

(C) James Adair 2024, All Rights Reserved

"""

# Hardware
from drivers.waveshare import epd7in5_V2 as waveshare
from drivers.huion import find_device as Huion

# System functions
from display import Display
from boot import boot
import logging

try:
    # ePaper initialization
    epaper = waveshare.EPD()  # Init display object
    display = Display(epaper)

    # Boot sequence
    boot(display)
    # display.save_to_file("test_boot.jpg")

except IOError as e:
    logging.error(e)
    
except KeyboardInterrupt:    
    logging.info("Initializing safe shutdown procedure")
    waveshare.epdconfig.module_exit(cleanup=True)
    exit()


# Rendering
import render.drawing
import render.pdf
import render.text

# Misc
import time
import traceback
import math
import io
from time import sleep
from threading import Thread


# Initialization
tablet = Huion()
logging.basicConfig(level=logging.DEBUG)




# Central logic
try:
    display.init_fast()
    display.clear()
    display.show(render.pdf.render_page("sample.pdf", 14))
    items = []
    stop = []
    t = Thread(target=render.drawing.draw_queue, args=(items, stop, display))
    t.start()
    while True:
        print("Draw now...")
        try:
            im, d, r = render.drawing.create_pen_image(tablet)
            items.append((im,d,r))
        except (TypeError, KeyboardInterrupt):
            stop += [1]
            t.join()
            break

except IOError as e:
    logging.error(e)
    
except KeyboardInterrupt:    
    logging.info("Initializing safe shutdown procedure")

finally:
    waveshare.epdconfig.module_exit(cleanup=True)
    display.save_to_file("test.jpg")
    exit()
