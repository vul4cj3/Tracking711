from PIL import Image
import pytesseract

tesseractOCR = 'please enter your tesseract.exe url'
# ex: C:\\Users\\username\\AppData\\Local\\Tesseract-OCR\\tesseract.exe


def getCaptchatxt(imgurl):
    img = Image.open(f'./captcha/{imgurl}')
    imgGray = img.convert('L')

    # set threshold
    threshold = 210
    # load pixel
    pixdata = imgGray.load()
    width, height = imgGray.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    # preview image
    binImg = imgGray
    # binImg.show()

    # load pixel
    pixdata = binImg.load()
    # get image size
    width, height = binImg.size
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            count = 0
            # top
            if pixdata[x, y - 1] > 245:
                count = count + 1
            # bottom
            if pixdata[x, y + 1] > 245:
                count = count + 1
            # left
            if pixdata[x - 1, y] > 245:
                count = count + 1
            # right
            if pixdata[x + 1, y] > 245:
                count = count + 1
            # top left
            if pixdata[x - 1, y - 1] > 245:
                count = count + 1
            # bottom left
            if pixdata[x - 1, y + 1] > 245:
                count = count + 1
            # top right
            if pixdata[x + 1, y - 1] > 245:
                count = count + 1
            # bottom right
            if pixdata[x + 1, y + 1] > 245:
                count = count + 1
            # clear noise
            if count > 4:
                pixdata[x, y] = 255
    # preview image
    nrImg = binImg
    # nrImg.show()

    pytesseract.pytesseract.tesseract_cmd = fr'{tesseractOCR}'
    text = pytesseract.image_to_string(nrImg, lang='eng')
    return text
