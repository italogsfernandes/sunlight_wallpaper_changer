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
from tzwhere import tzwhere


tzwhere = tzwhere.tzwhere()
header_msg = '*'*50 + """
py wallpaper changer
Developed by: italogsfernandes.github.io
""" +'*'*50
#pic_url  = "http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg"
#pic_url  = "https://static.die.net/earth/rectangular/1600.jpg"
pic_url  = "https://static.die.net/earth/mercator/1600.jpg"
qnt_max_de_erros = 30
tempo_espera_entre_erros = 10 # segundos

horarios_para_sincronizar = [10,40]
list_of_active_hours = []

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


def calcular_relacao_lat_pixel(l):
    # 45.7589 esta para 517
    #-18.9113 esta para 245
    # 517 para 887 - 517 = 370
    # 245 para 887 - 245 = 642
    # (45.7589 - l)/(45.7589 - (-18.9113)) = (517 - px) / (517 - 245)
    # tan = h / r
    # 0 -> +75º  == 443.5
    # 443.5 -> 0º == 0
    # 887 -> -75º  == -443.5
    #h1 = 443.5 - 517
    #h2 = 443.5 - 245
    #th1 = np.radians(45.7589)
    #th2 = np.radians(-18.9113)
    #R = (h2)/np.tan(th2)
    #l = 1.28333 # singapura
    #l = -22.953024 # rio
    #l = -18.9113 # uberlandia
    #l = 45.7589 # lyon
    #l = 48.859289 #paris
    #l = 71.256 # alaska
    #l = -74
    #R = 134
    #R = 1600 / (2*np.pi)
    #h = R*np.tan(th)
    #px = 880
    #px = 517 - ((517 - 245) * (45.7589 + l) / (45.7589 - (-18.9113)))
    R = 221
    th = np.radians(l)
    h = 0.99*R*np.log(np.tan((np.pi/4)+th/2))
    px = 443.5 - h
    return int(px)

def calcular_relacao_long_pixel(l):
    # 4.84139 esta para 769
    # -48.2622 esta para 541
    # 103.85 esta para 1217
    #l = -43.9542
    #l = 4.84139
    #l = -19.8157
    #l = 50.15
    #l = 0
    px = 1217 - ((1217 - 541) * (103.85 - l) / (103.85 - (-48.2622)))
    return int(px)

def convert_lat_long_to_px(lat, long):
    return (calcular_relacao_lat_pixel, calcular_relacao_long_pixel)

cities_data = [
        {
          'name' : 'Uberlândia',
          'fuso' : -3,
          'tz' : "Brazil/East",
          'Latitude': -18.9113,
          'Longitude': -48.2622,
          'location_pixels' : [517, 541],
          'tz_location_pixels' : [548, 552],
          'active': True
        },
        {
          'name' : 'Lyon',
          'fuso' : 2,
          'tz' : "Europe/Paris",
          'Latitude': 45.7589,
          'Longitude': 4.84139,
          'location_pixels' : [245, 769],
          'tz_location_pixels' : [262, 770],
          'active': True
        },
        {
          'name' : 'Singapura',
          'fuso' : 8,
          'tz' : "Asia/Singapore",
          'Latitude' : 1.28333,
          'Longitude': 103.85,
          'location_pixels' : [440, 1217],
          'tz_location_pixels' : [460, 1217],
          'active': True
        }
]

class city:
    def __init__(self, name, latitude=None, longitude=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.tz_str = self.get_tz_str_from_lat_long(self.latitude, self.longitude)
        self.location_pixels = self.get_location_from_lat_long(self.latitude, self.longitude)
        self.tz_location_pixels = self.location_pixels.copy()

        self.tz_location_pixels[0] = self.tz_location_pixels[0] + 10

        self.location_active = True
        self.tz_active = True
        self.name_active = False

    def get_tz_str_from_lat_long(self, lat, long):
        timezone_str = tzwhere.tzNameAt(lat, long)
        return timezone_str

    def get_location_from_lat_long(self, lat, long):
        R = 221
        th = np.radians(lat)
        h = 0.99*R*np.log(np.tan((np.pi/4)+th/2))
        px = 443.5 - h
        py = 1217 - ((1217 - 541) * (103.85 - long) / (103.85 - (-48.2622)))
        return [int(px), int(py)]

    def set_tz_loc_offset(self, x_of, y_of):
        self.tz_location_pixels[0] = self.location_pixels[0] + x_of
        self.tz_location_pixels[1] = self.location_pixels[1] + y_of

    def __repr__(self):
        return self.name + " - " + str(self.location_pixels) + " - " + self.tz_str

#'location_pixels' : [517, 541],
uberlandia = city('Uberlândia', latitude=-18.9113, longitude=-48.2622)
uberlandia.tz_location_pixels = [548, 552]

#'location_pixels' : [245, 769],
lyon = city('Lyon', latitude=45.7589,longitude=4.84139)
lyon.tz_location_pixels = [262, 770]

#'location_pixels' : [440, 1217],
singapura = city('Singapura', latitude=1.28333, longitude=103.85)

samara = city('Samara', 53.20007, 50.15)
samara.set_tz_loc_offset(-10,10)
#samara.name_active = True

kazan = city('Kazan', 55.78874, 49.12214)
kazan.set_tz_loc_offset(-10,10)
kazan.name_active = True
kazan.tz_active = True

moscou = city('Moscou', 55.7558, 37.6173)
moscou.set_tz_loc_offset(-25,-21)
moscou.name_active = False

bamberg = city('Bamberg', 49.8917, 10.8917)

#valognes
theotim = city('Theotim', 49.5167, -1.4667)
theotim.name_active = True
theotim.tz_active = False
#cities = [uberlandia, lyon, singapura, moscou, kazan, samara, bamberg]
cities = [uberlandia, lyon]

for city in cities:
    print(city)

'''
São Petersburgo
Kazan
Caliningrado
Sochi
Volgogrado
Saransk
Iecaterimburgo
Rostov-on-don
Níjni Novgorod
'''

rgb2gray = lambda x: np.dot(x[...,:3], [0.299, 0.587, 0.114])

def divided_by_24():
    city = lyon;
    world_image = misc.imread(wallpapers_folder+dowloaded_pic_name)
    ## colocando o marcador
    city_long_px = calcular_relacao_long_pixel(city.longitude)

    x = city.location_pixels[0]
    x_start = x - 10
    x_end = x + 10

    print(city.longitude)
    longs_before = list(np.arange(city.longitude,-180,-15))
    longs_afer = list(np.arange(city.longitude,180,15))
    list_longs = longs_before + longs_afer
    list_longs.remove(city.longitude)
    list_longs.remove(city.longitude)
    print(list_longs)
    for n in list_longs:
        city_long_px = calcular_relacao_long_pixel(n)
        y = city_long_px
        y_start = y - 1
        y_end = y + 1

        world_image[x_start:x_end,y_start:y_end, 0] = 255
        world_image[x_start:x_end,y_start:y_end, 1] = 0
        world_image[x_start:x_end,y_start:y_end, 2] = 0


    misc.imsave(wallpapers_folder+dowloaded_pic_name, world_image) # uses the Image module (PIL)

def divided_by_24_and_colored():
    city = lyon;
    world_image = misc.imread(wallpapers_folder+dowloaded_pic_name)
    ## colocando o marcador
    city_long_px = calcular_relacao_long_pixel(city.longitude)

    x = city.location_pixels[0]
    x_start = x - 10
    x_end = x + 10

    longs_before = list(np.arange(city.longitude,-180,-15))[::-1]
    longs_afer = list(np.arange(city.longitude,180,15))
    list_longs = longs_before + longs_afer
    list_longs.remove(city.longitude)
    #list_longs.remove(city.longitude)

    for n in list_longs:
        city_long_px = calcular_relacao_long_pixel(n)
        y = city_long_px
        y_start = y - 1
        y_end = y + 1

        world_image[x_start:x_end,y_start:y_end, 0] = 255
        world_image[x_start:x_end,y_start:y_end, 1] = 0
        world_image[x_start:x_end,y_start:y_end, 2] = 0

    #read_active_hours()

    tz = pytz.timezone(lyon.tz_str)
    dt_obj_now = datetime.now(tz=tz).strftime('%d/%m/%Y %H')
    new_minute = (datetime.now(tz=tz).minute // 30)*30

    datetime_object = datetime.strptime("%s:%d" % (dt_obj_now,new_minute), '%d/%m/%Y %H:%M')
    datetime_object = datetime_object.replace(tzinfo=tz)

    print("*"*50)
    print(datetime_object)
    print("*"*50)
    print(list_longs)
    print(list_longs.index(city.longitude))

    for dt_obj in list_of_active_hours:
        td = (datetime_object - dt_obj)
        hours = td.seconds / 3600
        print("diferenca_horaria: %.2f" % hours)

    misc.imsave(wallpapers_folder+dowloaded_pic_name, world_image) # uses the Image module (PIL)

def convert_hour_to_long(hour_to_convert):
    city_long = lyon.longitude
    diferenca = hour_now - hour_to_convert
    hour_now = 0
    if hour_to_convert == hour_now:
        return city_long

    if hour_to_convert > hora_minima and hour_to_convert < hour_now:
        return city_long - 15*diferenca


    return 0

def where_is_neymar():
    city = kazan
    world_image = misc.imread(wallpapers_folder+dowloaded_pic_name)
    pin_image = misc.imread(wallpapers_folder+'pin_locator_files/neymar.jpg')
    pin_image_gray = rgb2gray(pin_image)
    pin_image_mask = pin_image_gray < 230
    x = city.location_pixels[0]
    y = city.location_pixels[1]
    x_start = x - pin_image.shape[0] - 5
    y_start = y - int(pin_image.shape[1]/2)
    x_end = x_start + pin_image.shape[0]
    y_end = y_start + pin_image.shape[1]
    ## colocando o marcador
    piece_of_world = world_image[x_start:x_end,y_start:y_end] # seleciona uma peça
    piece_of_world[pin_image_mask] = pin_image[pin_image_mask] # coloca o marcador nela
    world_image[x_start:x_end,y_start:y_end] = piece_of_world # devolve para o todo

    misc.imsave(wallpapers_folder+dowloaded_pic_name, world_image) # uses the Image module (PIL)

def add_lat_and_log(equator=True, green=True):
    world_image = misc.imread(wallpapers_folder+dowloaded_pic_name)
    equator_px = calcular_relacao_lat_pixel(0)
    green_px = calcular_relacao_long_pixel(0)
    world_image[:,green_px, 0] = 255
    world_image[:,green_px, 1] = 255
    world_image[:,green_px, 2] = 255
    world_image[equator_px,:, 0] = 255
    world_image[equator_px,:, 1] = 255
    world_image[equator_px,:, 2] = 255
    misc.imsave(wallpapers_folder+dowloaded_pic_name, world_image) # uses the Image module (PIL)

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

def read_active_hours():
    for dt_obj in list_of_active_hours:
        list_of_active_hours.remove(dt_obj)

    tz = pytz.timezone(lyon.tz_str)
    with open(wallpapers_folder+'last_active_hours.txt','r') as my_file:
        print("reading active hours")
        file_line = my_file.readline()
        file_line = file_line[:-1]
        while len(file_line) > 5:
            #print("file line: " + file_line)
            datetime_object = datetime.strptime(file_line, '%d/%m/%Y %H:%M')
            datetime_object = datetime_object.replace(tzinfo=tz)
            list_of_active_hours.append(datetime_object)
            file_line = my_file.readline()
            file_line = file_line[:-1]

    print("dados de %d horas ativas lidos" % len(list_of_active_hours))

def clear_list_of_active_hours(dt_obj_now):
    for dt_obj in list_of_active_hours:
        td = (dt_obj_now - dt_obj)
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds % 3600 / 60.0
        if days >= 1:
            print("Days >1 -> removing %s" % dt_obj.strftime('%d/%m/%Y %H:%M'))
            list_of_active_hours.remove(dt_obj)
        elif dt_obj.hour == dt_obj_now.hour:
            if dt_obj.minute < 30 and dt_obj_now.minute < 30:
                # ja existe uma entrada correspondente
                print("minute<30 ja existe -> removing %s" % dt_obj.strftime('%d/%m/%Y %H:%M'))
                list_of_active_hours.remove(dt_obj)
            elif dt_obj.minute >= 30 and dt_obj_now.minute >= 30:
                # ja existe uma entrada correspondente
                print("minute>30 ja existe -> removing %s" % dt_obj.strftime('%d/%m/%Y %H:%M'))
                list_of_active_hours.remove(dt_obj)

def save_active_hour():
    tz = pytz.timezone(lyon.tz_str)
    print("******len horas_ativas= %d" % len(list_of_active_hours))
    read_active_hours()
    print("******len horas_ativas= %d" % len(list_of_active_hours))

    dt_obj_now = datetime.now(tz=tz)

    clear_list_of_active_hours(dt_obj_now)
    print("******len horas_ativas= %d" % len(list_of_active_hours))

    list_of_active_hours.append(dt_obj_now)
    print("******len horas_ativas= %d" % len(list_of_active_hours))

    with open(wallpapers_folder+'last_active_hours.txt','w+') as my_file:
        print("adding %d lines to file" % len(list_of_active_hours))
        for dt_obj in list_of_active_hours:
            my_file.write(dt_obj.strftime('%d/%m/%Y %H:%M')+"\n")

def image_download_routine():
    errors_count = 0
    while errors_count < qnt_max_de_erros:
        if(wget_pic()):
            print("Image downloaded with success.")
            print("Adding circles in the cities locations.")
            add_circles()
            print("Add hours next to cities.")
            add_hours()
            print("saving time to last_active_hours.txt")
            save_active_hour()
            print("adding lines of 1 hour")
            divided_by_24_and_colored()
            #where_is_neymar()
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

def add_circles(radius_px=6, width_px=2):
    world_image = misc.imread(wallpapers_folder+dowloaded_pic_name)
    color_background = np.zeros((radius_px*2,radius_px*2,3), dtype=world_image.dtype)
    color_background[:,:,0] = 255
    color_background[:,:,1] = 0#255
    color_background[:,:,2] = 0#255
    circle_X, circle_Y = np.ogrid[0:radius_px*2, 0:radius_px*2]
    circle_out_mask = (circle_X - radius_px) ** 2 + (circle_Y - radius_px) ** 2 < radius_px**2
    circle_in_mask = (circle_X - radius_px) ** 2 + (circle_Y - radius_px) ** 2 > (radius_px-width_px)**2
    circle_mask = circle_in_mask * circle_out_mask

    for city in cities:
        ## Determinando o retangulo onde estarão os marcadores
        x = city.location_pixels[0]
        y = city.location_pixels[1]
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
    for city in cities:
        if city.tz_active or city.name_active:
            ## Determinando o retangulo onde estarão os marcadores
            x = city.tz_location_pixels[0]
            y = city.tz_location_pixels[1]
            text = ""
            if city.name_active:
                text += city.name + " "
            if city.tz_active:
                tz = pytz.timezone(city.tz_str)
                text += datetime.now(tz=tz).strftime('%H:%M')

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
    #salve_image_in_log(str(time_now).split('.')[0].replace(':','-').replace(' ', '_'))

def main():
    print(header_msg)
    print("First run...")
    image_download_routine()
    while(True):
        main_loop()

if __name__ == '__main__':
    #'location_pixels' : convert_lat_long_to_px(1.28333, 103.85),
    main()
