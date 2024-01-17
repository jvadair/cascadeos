from PIL import Image,ImageDraw,ImageFont

def create_pen_image(tablet, thickness=1):
    try:
        tablet.start_driver()
        # Wait for pen down
        while not tablet.get_pen_data()[2]:
            pass
        stroke = []
        _domain = [int(tablet.get_pen_data()[0])]*2
        _range = [int(tablet.get_pen_data()[1])]*2
        while tablet.get_pen_data()[2]:
            data = tablet.get_pen_data()
            print(data)
            stroke.append(data)
            # Adjust domain
            if data[0] < _domain[0]:
                _domain[0] = int(data[0])
            elif data[0] > _domain[1]:
                _domain[1] = int(data[0])
            # Adjust range
            if data[1] < _range[0]:
                _range[0] = int(data[1])
            elif data[1] > _range[1]:
                _range[1] = int(data[1])
    except KeyboardInterrupt:
        tablet.stop_driver()
        return None

    tablet.stop_driver()
    while (_domain[1] - _domain[0]) % 8:
        _domain[1] += 1
    print(_domain, _range)

    try:
        img = Image.new("1", (_domain[1]-_domain[0],_range[1]-_range[0]), color=255)
        draw = ImageDraw.Draw(img)
        prev_point = stroke[0]
        for point in stroke:
            x1 = point[0]-_domain[0]
            y1 = point[1]-_range[0]
            x2 = prev_point[0]-_domain[0]
            y2 = prev_point[1]-_range[0]
            p = int(point[2]*thickness*8)
            # draw.ellipse((x-(p/2),y-(p/2),x+(p/2),y+(p/2)), fill=0)  # solid black point of variable thickness
            draw.line((x1,y1,x2,y2), fill=00, width=p)
            prev_point = point
        # im.save('test.jpg')
        return img, _domain, _range
    except KeyboardInterrupt:
        return None

def draw_queue(items, stop, display):  # Run this as a thread
    display.init_part()
    while not stop:
        try:
            item = items.pop(0)
            print(item[0].width, item[0].height)
            print(item[1][0], item[2][0], item[1][1], item[2][1])
            display.draw(item[0], (item[1][0], item[2][0], item[1][1], item[2][1]), preserve_below=True)
        except IndexError:
            pass