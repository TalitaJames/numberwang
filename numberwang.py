from PIL import Image, ImageDraw, ImageFont
from num2words import num2words
import numpy as np
import random


def random_wangweighted_number(words=True):
    '''
    returns a random number,
    weighted towards one digit numbers or specificly short floats,
    like in numberwang
    '''
    # Choose a number (mostly int, but sometimes float)

    typeNum = random.random()
    value = 0

    if typeNum < 0.30:
        value = random.randint(0, 9)
    elif typeNum < 0.50:
        value = random.randint(9, 99)
    elif typeNum < 0.75:
        value = random.randint(0, 999)
    else:
        value = f"{random.uniform(0, 99):.2f}".rstrip('0')

    # about a tenth of the time, change it to words
    if words and random.random() < 0.1 and not isinstance(value, str):
        value = num2words(value)

    return str(value)


def make_canvas_pillow(
    canvasSize=(1920, 1080), # (width, height) size of the image
    outputFile="numberwang_board.png", # output location
    numElements=25, # how many numbers
    backgroundColour = (255, 255, 255, 255), # background colour
    numberColours = ["#B30808", "#294FCA", #the colours the numbers may be
                     "#208A12", "#F1AD2E", "#5BD137",
                     "#E641D8", "#AF32E9", "#5CC3EC"],
    font_path="assets/Bauhaus93Regular.ttf", # bauhaus is std for numberwang
    overlap=False, # if the numbers are allowed to overlap
    words=True # if the board is allowed to contain words of numbers (ie "two")
):
    numbers = Image.new("RGBA", canvasSize, (0,0,0,0))
    fontSize = 125
    max_area_ratio = 0.10 # each number should take this much % of canvas max
    canvas_area = canvasSize[0] * canvasSize[1]

    for _ in range(numElements):
        element = random_wangweighted_number(words)

        # scale, rotate and place element on blank minimum sized png
        scale = max(np.random.normal(1, 0.4), 0.5) # mean = 1, std dev = 0.4
        size = int(scale*fontSize)
        font = ImageFont.truetype(font_path, size)

        rotation = np.random.normal(0, 15)  % 360
        colour = random.choice(numberColours)

        bbox = font.getbbox(element)
        element_w = bbox[2] - bbox[0]
        element_h = bbox[3] - bbox[1]

        # make a png with just the element
        element_img = Image.new("RGBA", (element_w, element_h), (0, 0, 0, 0))
        element_draw = ImageDraw.Draw(element_img)
        element_draw.text((0, 0), element, font=font, fill=colour, anchor="lt")


        # make sure the area isn't too big
        element_area = element_w * element_h
        if element_area > max_area_ratio * canvas_area:
            shrink_factor = 3
            element_img = element_img.resize((int(element_w//shrink_factor), int(element_h//shrink_factor)), resample=Image.Resampling.NEAREST)

        rotated_img = element_img.rotate(rotation, expand=True)
        element_w, element_h = rotated_img.size


        # find a non occupied spot for the element
        spotFound = False
        for _ in range(100):
            x = random.randint(0, canvasSize[0] - element_w)
            y = random.randint(0, canvasSize[1] - element_h)

            if overlap:
                break # overlap doesn't care about a "safe place"

            potentialPlacment = numbers.crop((x, y, x + element_w, y + element_h)).getchannel("A")

            # an empty bounding box means space is clear
            if potentialPlacment.getbbox() is None:
                spotFound = True
                break

        if spotFound or overlap:
            numbers.paste(rotated_img, (x, y), rotated_img)


    # add the numbers onto the coloured background
    background = Image.new("RGBA", canvasSize, backgroundColour)
    background.paste(numbers, (0, 0), numbers)

    background.save(outputFile)



if __name__ == "__main__":
    # Config
    outputFile = "numberwang_board.png"

    config = {
        "canvasSize":(1920, 1080),
        "outputFile":"out/numberwang_board.png",
        "numElements":30,
        "words":False,
        "overlap":False,
    }

    lightMode = {
        "backgroundColour" : "#FFFFFFFF",
        "numberColours" : ["#B30808", "#294FCA",
                     "#208A12", "#F1AD2E", "#5BD137",
                     "#E641D8", "#AF32E9", "#5CC3EC"]
    }
    darkPastel = {
        "backgroundColour" : "#272932FF",
        "numberColours" : ["#BAF2BB", "#BAF2D8", "#BAD7F2", "#F2BAC9", "#F2E2BA"]
    }


    # make_canvas_pillow(**config, **lightMode)
    make_canvas_pillow(**config, **darkPastel)

