import scipy as sp
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import textwrap
import os
from PIL import ImageOps

def animator(imageURL, imageText,idx):

    im = Image.open(imageURL)
    basewidth = 600
    im = im.resize([basewidth, basewidth], Image.ANTIALIAS)

    x = im.size[0]
    y = im.size[1]

    try:
        draw = ImageDraw.Draw(im,'RGBA')
    except ValueError:
        im = im.convert('RGBA')
        draw = ImageDraw.Draw(im,'RGBA')



    lines = textwrap.wrap(imageText)

    maxlen = max(len(s) for s in lines)
    long_line = [s for s in lines if len(s)==maxlen ]
    unique_line = list(set(long_line))
    unique_line = unique_line[0]

    font, font_color = font_type(im, unique_line)

    text_width, text_height = font.getsize(unique_line)

    region  = new_region(x,y)

    print "height",text_height
    x_text = 0.05*x
    y_text = 0.8*y + ((0.2*y)-(text_height*len(lines)))/2 - 5

    draw.polygon(region, (255,250,250,230))
    print y
    for line in lines:
        print "Text",line, y_text
        draw.text((x_text, y_text), line, font=font, fill= font_color)
        y_text += text_height + 5


    im.save(open('Stories/'+str(idx+1)+'.jpg','w'))



def font_type(image,txt):
    font_size = 1
    font_fname = 'fonts/Arial/Arialn.ttf'
    font_color = 'rgb(0,0,0)'

    font = ImageFont.truetype(font_fname, font_size)

    img_fraction = 0.9
    print img_fraction*image.size[0]
    while font.getsize(txt)[0] < (img_fraction*image.size[0]):
        font_size += 1
        font = ImageFont.truetype(font_fname, font_size)
    font_size -= 1

    font = ImageFont.truetype(font_fname, font_size )

    return font, font_color

def new_region(x,y):
    region = [(0,0.8*y), (0.8*x,0.8*y), (0.85*x,0.75*y), (x,0.75*y), (x,y),(0,y)]
    return region



# animator('/Users/gautamchheda/Desktop/StartupStudio/stock_images/shutterstock_121813225.jpg','Electrolytes tackle dehdration. Patients are required to take 20 mg of it a day.')
