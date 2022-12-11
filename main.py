import threading
import time
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
# Formulaire

EVENT_TIMEOUT = .01  # A very short timeout - seconds.
POLLING_DELAY = 1000  # How often to check search status - millisecs.

locator = Nominatim(user_agent="low-fuel")

# create tkinter window
root_tk = Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Carte des stations à proximité")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=.5, rely=.5, anchor=CENTER)

# set current widget position and zoom
map_widget.set_position(48.866667, 2.333333)  # Domicile
map_widget.set_zoom(13)

fenetrePrincipale = root_tk

name_entry: str = ""
street_entry: str = ""
post_code_entry: int = 0
city_entry: str = ""
radius_entry: float = 0.0

def printValue():
    global name_entry
    global street_entry
    global post_code_entry
    global city_entry
    global radius_entry
    name_entry = name_entry.get()
    street_entry = street_entry.get()
    post_code_entry = post_code_entry.get()
    city_entry = city_entry.get()
    radius_entry = radius_entry.get()
    fenetrePrincipale.destroy()

labl_0 = Label(fenetrePrincipale, text="Vos Infos Personnelles",width=20,font=("bold", 20))  
labl_0.place(x=240,y=53)
labl_0.pack()

name_label = Label(fenetrePrincipale, text = "Nom", font=("bold", 10))
name_entry = Entry(fenetrePrincipale)
name_label.place(x=200,y=130)  
name_entry.place(x=500,y=130)
name_label.pack()
name_entry.pack()

street_label = Label(fenetrePrincipale, text = "Numéro et nom de rue", font=("bold", 10))
street_entry = Entry(fenetrePrincipale)
street_label.place(x=200,y=230) 
street_entry.place(x=500,y=230)
street_label.pack()
street_entry.pack()

post_code_label = Label(fenetrePrincipale, text = "Code Postal", font=("bold", 10))
post_code_entry = Entry(fenetrePrincipale)
post_code_label.place(x=200,y=280)
post_code_entry.place(x=500,y=280)
post_code_label.pack()
post_code_entry.pack()

city_label = Label(fenetrePrincipale, text = "Ville", font=("bold", 10))
city_entry = Entry(fenetrePrincipale)
city_label.place(x=200,y=330)
city_entry.place(x=500,y=330)
city_label.pack()
city_entry.pack()

radius_label = Label(fenetrePrincipale, text = "Rayon d'action", font=("bold", 10))
radius_entry = Spinbox(fenetrePrincipale, from_=1, to=10)
radius_label.place(x=200,y=380)
radius_entry.place(x=500,y=380)
radius_label.pack()
radius_entry.pack()

submit = Button(fenetrePrincipale ,text="Envoyer...",width=20,bg='brown',fg='white',command=printValue)
submit.place(x=320,y=500)
submit.pack()

fenetrePrincipale.mainloop()

file_gif='KSYL.gif'

# create tkinter window
parent = Tk()
parent.geometry(f"{800}x{600}")
parent.title("Carte des stations à proximité")

lbl = Label()
lbl.pack()

parent.update()

idClient = uuid.uuid1()

user_address = AddressUser(idClient, str(street_entry),  str(post_code_entry), str(city_entry), str(radius_entry))

location = address_to_coord(user_address.street + ' ' + user_address.post_code + ' ' + user_address.city) 


user_address = AddressUser(idClient, str(street_entry),  str(post_code_entry), str(city_entry), str(radius_entry), location[0],location[1])
#infos gouvernementale

if location[1] > 0:
    location_1 = '+' + str(location[1])
radius = '+' + str(float(radius_entry) * 1000) 
url_data : str = 'https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download/?format=json&q=&geofilter.distance=' + str(location[0]) + ',' + location_1 + ',' + radius + '&timezone=Europe/Berlin&lang=fr'
path_of_file : str = 'info.gouv/prix-carburants.json'

my_sell_points: List[SellPoint] = ParseJson (url_data, path_of_file, user_address).station_list()

pdv: SellPoint

parent.destroy()
# create tkinter window
root_tk = Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Carte des stations à proximité")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=.5, rely=.5, anchor=CENTER)

# set current widget position and zoom
map_widget.set_position(location[0], location[1])  # Domicile
map_widget.set_zoom(13)

#set_first_marker
marker_1 = map_widget.set_position(location[0], location[1], marker=True, marker_color_circle = '#396D46', marker_color_outside = '#0C9F31', text_color = '#3F6990')
print(marker_1.position, marker_1.text)
marker_1.set_text("Point de départ")

for pdv in my_sell_points:
    print('\n')
    print("------------------------------------------------------------")
    print(pdv.idSP)
    print(pdv.name)
    print(str(pdv.address[0]) + ' ' + str(pdv.address[1]) + ' ' + str(pdv.address[2]) + ' ' + str(pdv.address[3]) + ' ' + str(pdv.address[4]))
    if pdv.week_hours.is_24_24:
        print("pompe(s) ouverte(s) 24h/24")
    else:
        if pdv.week_hours.day_hours[0][0][0] == "horaire non précisé":
            print("horaire non précisé")    
        else:
            for jour in range(0, 6):
                jour_en_lettre = str(pdv.week_hours.day_hours[0][jour][0])
                if pdv.week_hours.day_hours[0][jour][1]:
                    print(jour_en_lettre + " pas d'horaire spécifiée")
                else:
                    opening = pdv.week_hours.day_hours[0][jour][2][0]
                    closing = pdv.week_hours.day_hours[0][jour][2][1]
                    if opening.__len__() == 2:
                        print(jour_en_lettre + " ouverture le matin de " + opening[0].replace('.', 'h') + " à " + opening[1].replace('.', 'h') + " et l'après midi' de " + closing[0].replace('.', 'h') + " à " + closing[1].replace('.', 'h'))
                    else:
                        print(jour_en_lettre + " ouverture de " + opening.replace('.', 'h') + " à " + closing.replace('.', 'h'))
    prices_txt: str = ""
    prices_txt_geo: str = ""
    print("\n")
    for price in pdv.prices:
        if price != []:
            prices_txt += "Carburant " + str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\nDernière mise à jour du prix :" + str(price[2]) + "\n"          
            prices_txt_geo += str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\n"
    print(prices_txt)
    for service in pdv.services:
        print(str(service))
    print("Station à " + str(round(pdv.distance,2)).replace('.', ',') + ' km')
    print("------------------------------------------------------------")

    new_marker = map_widget.set_marker(pdv.address[3], pdv.address[4], text=pdv.name + '\n' + prices_txt_geo + '\n', text_color = '#3F6990')

map_widget.mainloop()