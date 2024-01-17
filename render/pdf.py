import fitz  # PyMuPDF, imported as fitz for backward compatibility reasons
from PIL import Image
import os
import io

BOOK_DIR = f"/home/{os.environ.get('USER')}/Bookshelf/"

def render_page(filename, page_number, margin=0):
    # Get page data
    doc = fitz.open(BOOK_DIR + filename)  # open document
    pix = doc[page_number].get_pixmap()
    data = pix.tobytes("jpg")
    im = Image.open(io.BytesIO(data))
    
    # Resize
    im = im.resize((480, 800-margin), Image.LANCZOS)

    # Black and white
    # im = im.convert('1')

    return im