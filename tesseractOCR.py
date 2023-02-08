from PIL import ImageGrab
from PIL import Image
from PIL import PngImagePlugin
from PIL import ImageOps
from PIL import ImageFilter

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


for i in range(1,6):
    ocred_txt = pytesseract.image_to_string(Image.open(f'zdj{i}.jpg'), lang='eng+pol')
    with open(f'zdj_({i})_enpl.txt',"w") as f:
        f.write(ocred_txt)

for i in range(1,4):
    ocred_txt = pytesseract.image_to_string(ImageOps.grayscale(Image.open(f'zdj{i}.jpg')), lang='eng+pol')
    with open(f'zdj_({i})_enplfilter.txt',"w") as f:
        f.write(ocred_txt)

for i in range(1,4):
    ocred_txt = pytesseract.image_to_string(Image.open(f'zdj{i}.jpg'), lang='pol')
    with open(f'zdj_({i})_onlyPL.txt',"w") as f:
        f.write(ocred_txt)

for i in range(1,4):
    ocred_txt = pytesseract.image_to_string(ImageOps.grayscale(Image.open(f'zdj{i}.jpg')), lang='pol')
    with open(f'zdj_({i})_filtergreyscale.txt',"w") as f:
        f.write(ocred_txt)


