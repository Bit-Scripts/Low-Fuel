import os
import threading
import time
from tkinter.ttk import Combobox
from typing import List
from geopy import Nominatim
from parsedata.parse_json import ParseJson
from tkinter import * 
import tkintermapview
import uuid
from PIL import Image, ImageTk
from itertools import count, cycle

from domain.user import AddressUser
from domain.data import SellPoint
from domain.logic import address_to_coord

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Formulaire

EVENT_TIMEOUT = .01  # A very short timeout - seconds.
POLLING_DELAY = 1000  # How often to check search status - millisecs.

locator = Nominatim(user_agent="low-fuel")

# create tkinter window

# Début formulaire
root_tk = Tk()
root_tk.geometry(f"{1150}x{800}")
root_tk.title("Carte des stations à proximité")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=.5, rely=.5, anchor=CENTER)

# set current widget position and zoom
map_widget.set_position(48.866667, 2.333333)  # Domicile
map_widget.set_zoom(13)

fenetrePrincipale = root_tk

firstFrame = Frame(fenetrePrincipale)
firstFrame.pack()

name_entry: str = ""
street_entry: str = ""
post_code_entry: int = 0
city_entry: str = ""
radius_entry: float = 0.0


def test():
    file_gif='KSYL.gif'
    idClient = uuid.uuid1()
    user_address = AddressUser(idClient, str(street_entry),  str(post_code_entry), str(city_entry), str(radius_entry))
    location = address_to_coord(user_address.street + ' ' + user_address.post_code + ' ' + user_address.city) 
    user_address = AddressUser(idClient, str(street_entry),  str(post_code_entry), str(city_entry), str(radius_entry), location[0],location[1])

    if location[1] > 0:
        location_1 = '+' + str(location[1])
    radius = '+' + str(float(radius_entry) * 1000) 
    url_data : str = 'https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download/?format=json&q=&refine.prix_nom=' + fuel_entry + '&geofilter.distance=' + str(location[0]) + ',' + location_1 + ',' + radius + '&timezone=Europe/Berlin&lang=fr'
    path_of_file : str = 'info.gouv/prix-carburants.json'

    parsejson = ParseJson (url_data, path_of_file, user_address)

    my_sell_points: List[SellPoint] = parsejson.station_list()

    pdv: SellPoint

    # set current widget position and zoom
    map_widget.set_position(location[0], location[1])  # Domicile
    map_widget.set_zoom(13)
    #set_first_marker
    marker_1 = map_widget.set_position(location[0], location[1], marker=True, marker_color_circle = '#396D46', marker_color_outside = '#0C9F31', text_color = '#3F6990')
    print(marker_1.position, marker_1.text)
    marker_1.set_text("Point de départ")

    i = 0

    for pdv in my_sell_points:
        print('\n')
        print("------------------------------------------------------------")
        print(pdv.idSP)
        text1 = pdv.name
        print(text1)
        text2 = str(pdv.address[0]) + ' ' + str(pdv.address[1]) + ' ' + str(pdv.address[2]) + ' ' + str(pdv.address[3]) + ' ' + str(pdv.address[4])
        print(text2)
        text5 = ""
        text6 = ""
        text7 = ""
        if pdv.week_hours.is_24_24:
            text3 = "pompe(s) ouverte(s) 24h/24"
            print(text3)
        else:
            if pdv.week_hours.day_hours[0][0][0] == "horaire non précisé":
                text3 = "horaire non précisé"
                print("horaire non précisé")    
            else:
                for jour in range(0, 6):
                    jour_en_lettre = str(pdv.week_hours.day_hours[0][jour][0])
                    if pdv.week_hours.day_hours[0][jour][1]:
                        text5 = jour_en_lettre + " pas d'horaire spécifiée"
                        print(text5)
                    else:
                        opening = pdv.week_hours.day_hours[0][jour][2][0]
                        closing = pdv.week_hours.day_hours[0][jour][2][1]
                        if opening.__len__() == 2:
                            text6 = jour_en_lettre + " ouverture le matin de " + opening[0].replace('.', 'h') + " à " + opening[1].replace('.', 'h') + " et l'après midi' de " + closing[0].replace('.', 'h') + " à " + closing[1].replace('.', 'h')
                            print(text6)
                        else:
                            text7 = jour_en_lettre + " ouverture de " + opening.replace('.', 'h') + " à " + closing.replace('.', 'h')
                            print(text7)
        prices_txt: str = ""
        prices_txt_geo: str = ""
        print("\n")
        for price in pdv.prices:
            if price != []:
                prices_txt += "Carburant " + str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\nDernière mise à jour du prix :" + str(price[2]) + "\n"          
                prices_txt_geo += str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\n"
        print(prices_txt)
        proposed_services: str = ""
        for service in pdv.services:
            proposed_services += str(service) + '\n'
            print(str(proposed_services))
        text8 = "Station à " + str(round(pdv.distance,2)).replace('.', ',') + ' km'
        print(text8)
        print("------------------------------------------------------------")

        data_text = text1 + '\n' + text2 + '\n' + text3 + '\n' + text5 + '\n' + text6 + '\n' + text7 + '\n' + prices_txt + '\n' + proposed_services + '\n' + text8
            # Open an Image
        img = Image.open('image/fuel_gauge_texts.jpg')
        
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)
        
        # Custom font style and font size
        myFont = ImageFont.truetype('AcariSans-Regular.ttf', 12)
        
        # Add Text to an image
        I1.text((5, 5), data_text, font=myFont, fill =(255, 255, 255))
        
        # Save the edited image
        low_fuel_image = f'image/fuel_gauge_texts_{i}.jpg'
        img.save(low_fuel_image)

        time_to_wait = 10
        time_counter = 0
        while not os.path.exists(low_fuel_image):
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:break
        
        im = Image.open(low_fuel_image)
        ph = ImageTk.PhotoImage(im)

        if pdv.name == parsejson.get_low_price_name():
            new_marker = map_widget.set_marker(pdv.address[3], pdv.address[4], marker_color_circle = '#736A7C', marker_color_outside = '#8551BF', text=pdv.name + '\n' + prices_txt_geo + '\n', text_color = '#FF0000', image = ph, image_zoom_visibility=(15, float("inf")))
            #new_marker.hide_image(True)
        else:
            new_marker = map_widget.set_marker(pdv.address[3], pdv.address[4], text=pdv.name + '\n' + prices_txt_geo + '\n', text_color = '#3F6990', image = ph, image_zoom_visibility=(15, float("inf")))
            #new_marker.hide_image(True)

        i += 1

def printValue():
    global street_entry
    global post_code_entry
    global city_entry
    global radius_entry
    global fuel_entry
    street_entry = street_entry.get()
    post_code_entry = post_code_entry.get()
    city_entry = city_entry.get()
    radius_entry = radius_entry.get()
    fuel_entry = fuel_entry.get()
    firstFrame.pack_forget()
    test()

    # ici 

labl_0 = Label(firstFrame, text="Vos Infos Personnelles",width=20,font=("bold", 20))  
labl_0.place(x=240,y=53)
labl_0.pack()

street_label = Label(firstFrame, text = "Numéro et nom de rue", font=("bold", 10))
street_entry = Entry(firstFrame)
street_label.place(x=200,y=230) 
street_entry.place(x=500,y=230)
street_label.pack()
street_entry.pack()

post_code_label = Label(firstFrame, text = "Code Postal", font=("bold", 10))
post_code_entry = Entry(firstFrame)
post_code_label.place(x=200,y=280)
post_code_entry.place(x=500,y=280)
post_code_label.pack()
post_code_entry.pack()

city_label = Label(firstFrame, text = "Ville", font=("bold", 10))
city_entry = Entry(firstFrame)
city_label.place(x=200,y=330)
city_entry.place(x=500,y=330)
city_label.pack()
city_entry.pack()

radius_label = Label(firstFrame, text = "Rayon d'action", font=("bold", 10))
radius_entry = Spinbox(firstFrame, from_=1, to=10)
radius_label.place(x=200,y=380)
radius_entry.place(x=500,y=380)
radius_label.pack()
radius_entry.pack()

list_fuel = ["SP95", "E85","Gazole","SP98","GPLc","E10"]
fuel_label = Label(firstFrame, text = "Choix du Carburant", font=("bold", 10))
fuel_entry = Combobox(firstFrame, values=list_fuel)
fuel_entry.current(0)
fuel_label.place(x=200,y=430)
fuel_entry.place(x=500,y=430)
fuel_label.pack()
fuel_entry.pack()

submit = Button(firstFrame ,text="Envoyer...",width=20,bg='brown',fg='white',command=printValue)
submit.place(x=320,y=550)
submit.pack()

fenetrePrincipale.mainloop()

# Fin de formulaire
map_widget.mainloop()