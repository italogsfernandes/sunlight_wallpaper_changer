#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests # Download
from time import sleep # time sleep during execution
from datetime import datetime, timedelta # sincronizando
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
#pic_url  = "http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg"
#pic_url  = "https://static.die.net/earth/rectangular/1600.jpg"
pic_url  = "https://static.die.net/earth/mercator/1600.jpg"
qnt_max_de_erros = 30 
tempo_espera_entre_erros = 10 # segundos

horarios_para_sincronizar = [8,38]

wallpapers_folder = '/home/italo/Images/Wallpapers/'
log_folder = 'log/'
font_name = 'pin_locator_files/micross.ttf'

if os.name == 'nt':
    print("Running on windows system")
    wallpapers_folder = 'D:/Users/italo/Pictures/Wallpapers/'
    wallpapers_folder = wallpapers_folder.replace('/', '\\')
    log_folder = log_folder.replace('/', '\\')
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
          'tz_location_pixels' : [460, 1217],
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
    while errors_count < qnt_max_de_erros:
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
            print("Waiting "+tempo_espera_entre_erros+"s to a new try...")
            sleep(tempo_espera_entre_erros)

def salve_image_in_log(time_str):
    print("****LOGGING IMAGE FILE: " + time_str + "****")
    source_file = wallpapers_folder+wallpaper_pic_name
    copied_file = wallpapers_folder+log_folder+time_str+".jpg"
    if os.name == 'nt':
        os.system('copy ' + source_file + ' ' +  copied_file);
    else:
        os.system('cp ' + source_file + ' ' +  copied_file);

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
            text = datetime.now(tz=tz).strftime('%H:%M')
            draw.text((y, x), text,(255,0,0),font=font)

    #plt.imshow(img)
    img.save(wallpapers_folder+dowloaded_pic_name)

def commit_changes():
    os.remove(wallpapers_folder+wallpaper_pic_name)
    os.rename(wallpapers_folder+dowloaded_pic_name, wallpapers_folder+wallpaper_pic_name)
    if os.name == 'nt':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpapers_folder+wallpaper_pic_name, 3)

def create_gif():
    #https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    pass

def calcular_espera(minuto_agora, minuto_referencia):
    espera = 0
    if minuto_agora < minuto_referencia:
        espera = minuto_referencia - minuto_agora
    else:
        espera = (60 - minuto_agora) + minuto_referencia
    return espera

def main_loop():
    time_now = datetime.now()
    minute_now = time_now.minute

    espera_para_sincronizar = min([calcular_espera(minute_now, minuto_sinc) for minuto_sinc in horarios_para_sincronizar])
    print("Wainting "+str(espera_para_sincronizar)+" minutes until "+str(datetime.now() + timedelta(minutes=espera_para_sincronizar))+".")
    sleep(60*espera_para_sincronizar)

    print("Sincronizando - " + str(datetime.now()) + ".")
    image_download_routine()
    salve_image_in_log(str(time_now).split('.')[0].replace(':','-').replace(' ', '_'))
    
def main():
    print(header_msg)
    print("First run...")
    image_download_routine()
    while(True):
        main_loop()

if __name__ == '__main__':
    main()
