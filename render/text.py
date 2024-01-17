from PIL import Image,ImageDraw,ImageFont

# Fonts
font24 = ImageFont.truetype('fonts/UbuntuMono-Regular.ttf', 24)
font18 = ImageFont.truetype('fonts/UbuntuMono-Regular.ttf', 18)

def format_text(text, font_size, screen_width, padding=2):  # Only works for monospace fonts
    max_chars = screen_width/(0.5*font_size)-(padding*2)
    out = [""]
    text = text.split(" ")
    for word in text:
        if len(out[-1]) + len(word)+1 < max_chars:
            out[-1] += word + " "
        else:
            out.append(word)
    return "\n".join(["{a}{b}{a}".format(a=" "*padding, b=i) for i in out])

def render_text(epaper, text, font_size=24):
    img = Image.new('1', (epaper.height, epaper.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((0, 0), render_text(text, font_size, epaper.height), font = font24, fill = 0)
    return img