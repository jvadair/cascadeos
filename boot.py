from PIL import Image,ImageDraw,ImageFont

def boot(display):
    display.init()

    img = Image.open('static/img/bootsplash.png')
    display.show(img)