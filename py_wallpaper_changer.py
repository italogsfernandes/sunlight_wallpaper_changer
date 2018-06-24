#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests # Download
from time import sleep # time sleep during execution
from datetime import datetime # sincronizando
from PIL import Image # Adding text
from PIL import ImageFont # Adding text
from PIL import ImageDraw # Adding text
import pytz # Adding timezone text
import ctypes # Altering windows dlls
from scipy import misc # Opening and clossing
import numpy as np

header_msg = '*'*50 + """
py wallpaper changer
Developed by: italogsfernandes.github.io
""" +'*'*50
pic_url  = "http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg"

wallpapers_folder = '/home/italo/Images/Wallpapers/'
font_name = 'pin_locator_files/micross.ttf'

if os.name == 'nt':
    print("Running on windows system")
    wallpapers_folder = 'D:/Users/italo/Pictures/Wallpapers/'
    wallpapers_folder = wallpapers_folder.replace('/', '\\')
    font_name = font_name.replace('/', '\\')

dowloaded_pic_name = 'world.jpg'
wallpaper_pic_name = 'world_sunlight_Wallpaper.jpg'

cities_data = [
        {
          'name' : 'Uberlândia',
          'fuso' : -3,
          'tz' : "Brazil/East",
          'location_pixels' : [517, 541],
          'tz_location_pixels' : [548, 552],
          'active': True
        },
        {
          'name' : 'Lyon',
          'fuso' : 2,
          'tz' : "Europe/Paris",
          'location_pixels' : [245, 769],
          'tz_location_pixels' : [262, 770],
          'active': True
        },
        {
          'name' : 'Singapura',
          'fuso' : 8,
          'tz' : "Asia/Singapore",
          'location_pixels' : [440, 1217],
          'tz_location_pixels' : [440, 1217],
          'active': True
        }
]
def wget_pic():
    response_ok = True
    with open(wallpapers_folder + dowloaded_pic_name, 'wb') as handle:
        print(datetime.now())
        print("Downloading a new picture and saving as %s." % dowloaded_pic_name)
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            response_ok = False
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return response_ok

def image_download_routine():
    errors_count = 0
    while errors_count < 30:
        if(wget_pic()):
            print("Image downloaded with success.")
            print("Adding circles in the cities locations.")
            add_circles()
            print("Adding hours next to cities.")
            add_hours()
            print("Renaming file.")
            commit_changes()
            break
        else:
            print("Error during image download.")
            errors_count = errors_count + 1
            print("Error count: %d" % errors_count)
            print("Waiting 10s to a new try...")
            sleep(10)

def add_circles(radius_px=6, width_px=1):
	world_image = misc.imread(wallpapers_folder+dowloaded_pic_name)
	color_background = np.zeros((radius_px*2,radius_px*2,3), dtype=world_image.dtype)
	color_background[:,:,0] = 255
	circle_X, circle_Y = np.ogrid[0:radius_px*2, 0:radius_px*2]
	circle_out_mask = (circle_X - radius_px) ** 2 + (circle_Y - radius_px) ** 2 < radius_px**2
	circle_in_mask = (circle_X - radius_px) ** 2 + (circle_Y - radius_px) ** 2 > (radius_px-width_px)**2
	circle_mask = circle_in_mask * circle_out_mask

	for city in cities_data:
	    ## Determinando o retangulo onde estarão os marcadores
	    x = city['location_pixels'][0]
	    y = city['location_pixels'][1]
	    x_start = x - radius_px
	    y_start = y - radius_px
	    x_end = x_start + radius_px*2
	    y_end = y_start + radius_px*2

	    ## colocando o marcador
	    piece_of_world = world_image[x_start:x_end,y_start:y_end] # seleciona uma peça
	    piece_of_world[circle_mask] = color_background[circle_mask] # coloca o marcador nela
	    world_image[x_start:x_end,y_start:y_end] = piece_of_world # devolve para o todo

	misc.imsave(wallpapers_folder+dowloaded_pic_name, world_image) # uses the Image module (PIL)

def add_hours(font_size=18):
    img = Image.open(wallpapers_folder+dowloaded_pic_name)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(wallpapers_folder+font_name, font_size)
    for city in cities_data:
        if city['active']:
            ## Determinando o retangulo onde estarão os marcadores
            x = city['tz_location_pixels'][0]
            y = city['tz_location_pixels'][1]
            tz = pytz.timezone(city['tz'])
            text = str(datetime.now(tz=tz).hour) + " hrs"
            draw.text((y, x), text,(255,0,0),font=font)

    #plt.imshow(img)
    img.save(wallpapers_folder+dowloaded_pic_name)

def commit_changes():
    os.remove(wallpapers_folder+wallpaper_pic_name)
    os.rename(wallpapers_folder+dowloaded_pic_name, wallpapers_folder+wallpaper_pic_name)
    if os.name == 'nt':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpapers_folder+wallpaper_pic_name, 3)

def main_loop():
    minute_now = datetime.now().second
    if minute_now > 5 and minute_now <= 11: # 6 min tolerance
        msg = "Sincronizado - " + str(datetime.now()) + "."
        print('*'*len(msg))
        print(msg)
        print('*'*len(msg))
        image_download_routine()

        if minute_now < 9:
            print("Wainting 61 minutes")
            sleep(60*61)
        else:
            print("Wainting 59 minutes")
            sleep(60*59)
    else:
        print("Não Sincronizado - " + str(datetime.now()) + ".")
        print("Wainting 5 minutes")
        sleep(60*5)

def main():
    print(header_msg)
    print("First run...")
    image_download_routine()
    while(True):
        main_loop()

if __name__ == '__main__':
    main()
