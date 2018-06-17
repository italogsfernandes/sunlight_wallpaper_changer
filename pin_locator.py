# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc # Opening and clossing
#------------------------------------------------------------------------------
## Opening and writing to image files (2.6.1.)
# ------------------------------------------------------------------------------
def save_image(input_image,name=None,extension='.png',folder=None):
    """
    Save a image in a determined format and folder
    """
    complete_file_name = name + extension
    if not folder is None:
        complete_file_name = folder + complete_file_name
    misc.imsave(complete_file_name, input_image) # uses the Image module (PIL)

def read_image(name,extension='.png',folder=None):
    """
    Reads a image from file.
    Other options
    -------------
    Opening raw files
    >>> face_from_raw = np.fromfile('face.raw', dtype=np.uint8)
    >>> face_from_raw.shape = (768, 1024, 3)
    Need to know the shape and dtype of the image (how to separate data bytes).

    For large data, use np.memmap for memory mapping:
    >>> face_memmap = np.memmap('face.raw', dtype=np.uint8, shape=(768, 1024, 3))
    (data are read from the file, and not loaded into memory)

    Working on a list of image files
    >> from glob import glob
    >> filelist = glob('random*.png')
    """
    complete_file_name = name + extension
    if not folder is None:
       complete_file_name = folder + complete_file_name

    output_image = misc.imread(complete_file_name)
    return output_image


cities_data = [
        {
          'name' : 'Uberlândia',
          'fuso' : -3,
          'tz' : "Brazil/East",
          'location_pixels' : [517, 541]
        },
        {
          'name' : 'Lyon',
          'fuso' : 2,
          'tz' : "Europe/Paris",
          'location_pixels' : [246, 778]
        },
        {
          'name' : 'Singapura',
          'fuso' : 8,
          'tz' : "Asia/Singapore",
          'location_pixels' : [440, 1217]
        }
]

## Abrindo as imagens
world_image = read_image('/home/italo/Images/Wallpapers/world','.jpg')
#world_image = read_image('brasil_test_image','.jpg')
pin_image = read_image('/home/italo/Images/Wallpapers/pin_locator_files/pin_icon(15x20)','.jpg')
rgb2gray = lambda x: np.dot(x[...,:3], [0.299, 0.587, 0.114])
pin_image_gray = rgb2gray(pin_image)

## Criando mascara
# Olhando pelo histograma um limiar de 215 parece bom
#from scipy_toolbox import show_hist
#show_hist(pin_image_gray)
pin_image_mask = pin_image_gray < 120

## Opcional: Mostrar
#plt.imshow(world_image)
#plt.imshow(pin_image)

for city in cities_data:
    ## Determinando o retangulo onde estarão os marcadores
    x = city['location_pixels'][0]
    y = city['location_pixels'][1]

    x_start = x - pin_image.shape[0]
    y_start = y - int(pin_image.shape[1]/2)

    x_end = x_start + pin_image.shape[0]
    y_end = y_start + pin_image.shape[1]

    ## colocando o marcador
    piece_of_world = world_image[x_start:x_end,y_start:y_end] # seleciona uma peça
    piece_of_world[pin_image_mask] = pin_image[pin_image_mask] # coloca o marcador nela
    world_image[x_start:x_end,y_start:y_end] = piece_of_world # devolve para o todo

## Opcional: Visualizando o resultado
#plt.imshow(world_image)

## E por fim, salvar o resultado
save_image(world_image, '/home/italo/Images/Wallpapers/world_pinned', '.jpg')

## adicionando texto
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import pytz

img = Image.open("/home/italo/Images/Wallpapers/world_pinned.jpg")
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("/home/italo/Images/Wallpapers/pin_locator_files/micross.ttf", 20)
for city in cities_data:
    ## Determinando o retangulo onde estarão os marcadores
    x = city['location_pixels'][0]
    y = city['location_pixels'][1]
    tz = pytz.timezone(city['tz'])
    text = str(datetime.now(tz=tz).hour) + " hrs"
    draw.text((y, x), text,(255,0,0),font=font)

#plt.imshow(img)
img.save('/home/italo/Images/Wallpapers/world_time.jpg')
