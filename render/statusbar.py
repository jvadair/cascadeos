from PIL import Image,ImageDraw,ImageFont

# Fonts
font10 = ImageFont.truetype('fonts/UbuntuMono-Regular.ttf', 10)

def generate_status_bar():
    im = Image.new("1", )