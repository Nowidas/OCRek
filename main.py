import time
import sys
import os

sys.path.append(os.path.abspath("SO_site-packages"))

import pyperclip
from PIL import ImageGrab
from PIL import Image
from PIL import PngImagePlugin
from PIL import ImageOps

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from windows_logic import (
    init_getmessageinput,
    getmessageinput,
    registerKeys,
    get_TLUMACZ_MOD,
    get_ON_OFF,
)
from sys_trayicon import init_trayicon


def compare_images(input_image, output_image):
    # compare image dimensions (assumption 1)
    if input_image.size != output_image.size:
        return False
    rows, cols = input_image.size
    # compare image pixels (assumption 2 and 3)
    for row in range(rows):
        for col in range(cols):
            input_pixel = input_image.getpixel((row, col))
            output_pixel = output_image.getpixel((row, col))
            if input_pixel != output_pixel:
                return False
    return True


def main():
    recent_value = pyperclip.paste()
    im = ImageGrab.grabclipboard()
    trayico = init_trayicon()
    msg = init_getmessageinput()
    registerKeys()
    # print('Program Started !')
    # print('tlumacz mod: on')

    while True:
        tmp_value = pyperclip.paste()
        tmp_im = ImageGrab.grabclipboard()
        # print("|txt-",recent_value,"|img-",im,"|")
        getmessageinput(msg)
        trayico.cykl()
        # print("|txt-",tmp_value,"|img-",tmp_im,"|")
        # print("==================================")
        ## OCR photo to text if needed
        if (im is None and type(tmp_im) is PngImagePlugin.PngImageFile) or (
            type(im) is PngImagePlugin.PngImageFile
            and type(tmp_im) is PngImagePlugin.PngImageFile
            and not compare_images(tmp_im, im)
        ):
            im = tmp_im
            im.save("toOCR.png", "PNG")
            # print("saved")
            if get_ON_OFF():
                # sometimes better without greyscale
                ocred_txt = pytesseract.image_to_string(
                    Image.open("toOCR.png"), lang="eng+pol"
                )
                pyperclip.copy(ocred_txt.strip())
        ## Grab text and show translated
        if (recent_value == "" and tmp_value != "") or (
            tmp_value != "" and recent_value != "" and recent_value != tmp_value
        ):
            recent_value = tmp_value
            # os.system('cls')
            # print(recent_value.strip())

        time.sleep(0.1)


if __name__ == "__main__":
    main()
