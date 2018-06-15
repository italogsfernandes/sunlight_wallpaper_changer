# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy_toolbox import read_image, save_image

cities_data = [
        { 
          'name' : 'Uberlândia',
          'fuso' : -3,
          'location_pixels' : [517, 541]
        },
        { 
          'name' : 'Lyon',
          'fuso' : 2,
          'location_pixels' : [246, 778]
        },
        { 
          'name' : 'Singapura',
          'fuso' : 8,
          'location_pixels' : [440, 1217]
        }
]

## Abrindo as imagens
world_image = read_image('/home/italo/Images/Wallpapers/world','.jpg')
#world_image = read_image('brasil_test_image','.jpg')
pin_image = read_image('/home/italo/Images/Wallpapers/pin_icon(15x20)','.jpg')
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

img = Image.open("/home/italo/Images/Wallpapers/world_pinned.jpg")
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("/home/italo/Images/Wallpapers/micross.ttf", 20)
for city in cities_data:
    ## Determinando o retangulo onde estarão os marcadores
    x = city['location_pixels'][0]
    y = city['location_pixels'][1]
    text = str(datetime.utcnow().hour + city['fuso']) + " hrs"
    draw.text((y, x), text,(255,0,0),font=font)

#plt.imshow(img)
img.save('/home/italo/Images/Wallpapers/world_time.jpg')



