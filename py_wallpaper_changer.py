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
          'active': True
        },
        {
          'name' : 'Lyon',
          'fuso' : 2,
          'tz' : "Europe/Paris",
          'location_pixels' : [245, 769],
          'active': True
        },
        {
          'name' : 'Singapura',
          'fuso' : 8,
          'tz' : "Asia/Singapore",
          'location_pixels' : [440, 1217],
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
            #add_pins()
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

def add_hours(font_size=16):
    img = Image.open(wallpapers_folder+dowloaded_pic_name)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(wallpapers_folder+font_name, font_size)
    for city in cities_data:
        if city['active']:
            ## Determinando o retangulo onde estarão os marcadores
            x = city['location_pixels'][0]
            y = city['location_pixels'][1]
            tz = pytz.timezone(city['tz'])
            text = str(datetime.now(tz=tz).hour) + " hrs"
            draw.text((y, x), text,(255,0,0),font=font)

    #plt.imshow(img)
    img.save(wallpapers_folder+dowloaded_pic_name)

def commit_changes():
    os.rename(wallpapers_folder+dowloaded_pic_name, wallpapers_folder+wallpaper_pic_name)

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
