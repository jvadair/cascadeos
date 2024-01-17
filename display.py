from PIL import Image

class Init:
    class default: pass
    class fast: pass
    class part: pass

class Display:
    def __init__(self, epaper):
        self.epaper = epaper
        self.img = Image.new("1", (self.epaper.width, self.epaper.height), 0xFF)  # Blank white by default
        self.epaper.init()
        self.mode = Init.default
    
    def show(self, img):
        if img.width == self.epaper.height and img.height == self.epaper.width:
            self.img = img.rotate(270, expand=True)  # Store img in memory
        else:
            self.img = img
        self.epaper.display(self.epaper.getbuffer(img))

    def draw(self, img, rect, preserve_below=False):
        if preserve_below:
            # Make white transparent
            self.img = self.img.convert("RGBA")  # Allow pasting transparent
            img = img.convert("RGBA")
            data = img.getdata()
            newData = []
            for item in data:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            img.save("transparent_test.png")
        
        if preserve_below:
            self.img.paste(img, rect[0:2], mask=img)
            self.img.save("test_pls.png")
            self.img = self.img.convert("1")  # Back to black and white
            img = self.img.crop(rect)
        else:
            self.img.paste(img, rect[0:2])
        self.epaper.display_Partial(self.epaper.getbuffer(img, force_dimensions=False),*rect)

    def init(self):
        self.init_mode = Init.default
        self.epaper.init()

    def init_fast(self):
        self.init_mode = Init.fast
        self.epaper.init_fast()

    def init_part(self):
        self.init_mode = Init.part
        self.epaper.init_part()
    
    def clear(self):
        self.img = Image.new("1", (self.epaper.width, self.epaper.height), 0xFF)
        self.epaper.Clear()

    def sleep(self):
        self.epaper.sleep()
    
    def save_to_file(self, filename):
        self.img.save(filename)
