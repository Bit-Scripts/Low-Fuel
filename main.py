from ctypes import windll
import os
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


EVENT_TIMEOUT = .01  # A very short timeout - seconds.
POLLING_DELAY = 1000  # How often to check search status - millisecs.

locator = Nominatim(user_agent="low-fuel")

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

'''
def set_appwindow(mainWindow):  # Pour afficher l'icon dans la barre des taches

    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    mainWindow.wm_withdraw()
    mainWindow.after(10, mainWindow.wm_deiconify)
'''

class Main(Tk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{1150}x{800}")
        self.title("Carte des stations à proximité")

        # create map widget
        self.map_widget = tkintermapview.TkinterMapView(self, width=1150, height=800, corner_radius=0)
        self.map_widget.place(relx=.5, rely=.5, anchor=CENTER)

        # set current widget position and zoom
        self.map_widget.set_position(48.866667, 2.333333)  # Domicile
        self.map_widget.set_zoom(13)

        self.frame = Frame(self)
        self.frame.pack(expand=YES)

        # Définition de variable simple
        self.name_entry: str = ""
        self.street_entry: str = ""
        self.post_code_entry: int = 0
        self.city_entry: str = ""
        self.radius_entry: float = 0.0

        self.labl_0 = Label(self.frame, text="Vos Infos Personnelles",width=20,font=("bold", 20))  
        self.labl_0.place(x=240,y=53)
        self.labl_0.pack()

        self.street_label = Label(self.frame, text = "Numéro et nom de rue", font=("bold", 10))
        self.street_entry = Entry(self.frame)
        self.street_label.place(x=200,y=230) 
        self.street_entry.place(x=500,y=230)
        self.street_label.pack()
        self.street_entry.pack()

        self.post_code_label = Label(self.frame, text = "Code Postal", font=("bold", 10))
        self.post_code_entry = Entry(self.frame)
        self.post_code_label.place(x=200,y=280)
        self.post_code_entry.place(x=500,y=280)
        self.post_code_label.pack()
        self.post_code_entry.pack()

        self.city_label = Label(self.frame, text = "Ville", font=("bold", 10))
        self.city_entry = Entry(self.frame)
        self.city_label.place(x=200,y=330)
        self.city_entry.place(x=500,y=330)
        self.city_label.pack()
        self.city_entry.pack()

        self.radius_label = Label(self.frame, text = "Rayon d'action", font=("bold", 10))
        self.radius_entry = Spinbox(self.frame, from_=1, to=10)
        self.radius_label.place(x=200,y=380)
        self.radius_entry.place(x=500,y=380)
        self.radius_label.pack()
        self.radius_entry.pack()

        self.list_fuel = ["SP95", "E85","Gazole","SP98","GPLc","E10"]
        self.fuel_label = Label(self.frame, text = "Choix du Carburant", font=("bold", 10))
        self.fuel_entry = Combobox(self.frame, values=self.list_fuel)
        self.fuel_entry.current(0)
        self.fuel_label.place(x=200,y=430)
        self.fuel_entry.place(x=500,y=430)
        self.fuel_label.pack()
        self.fuel_entry.pack()

        self.submit = Button(self.frame ,text="Envoyer...",width=20,bg='brown',fg='white',command=self.printValue)
        self.submit.place(x=320,y=550)
        self.submit.pack()
           
        # Affichage fenêtre
        center(self)
        #set_appwindow(self)
        self.mainloop()
        self.map_widget()
        
    
    def printValue(self):
        self.street_entry = self.street_entry.get()
        self.post_code_entry = self.post_code_entry.get()
        self.city_entry = self.city_entry.get()
        self.radius_entry = self.radius_entry.get()
        self.fuel_entry = self.fuel_entry.get()
        self.frame.pack_forget()
        self.test()

    
    def test(self):
        file_gif='KSYL.gif'
        idClient = uuid.uuid1()
        user_address = AddressUser(idClient, str(self.street_entry),  str(self.post_code_entry), str(self.city_entry), str(self.radius_entry))
        location = address_to_coord(user_address.street + ' ' + user_address.post_code + ' ' + user_address.city) 
        user_address = AddressUser(idClient, str(self.street_entry),  str(self.post_code_entry), str(self.city_entry), str(self.radius_entry), location[0],location[1])

        if location[1] > 0:
            location_1 = '+' + str(location[1])
        radius = '+' + str(float(self.radius_entry) * 1000) 
        url_data : str = 'https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download/?format=json&q=&refine.prix_nom=' + self.fuel_entry + '&geofilter.distance=' + str(location[0]) + ',' + location_1 + ',' + radius + '&timezone=Europe/Berlin&lang=fr'
        path_of_file : str = 'info.gouv/prix-carburants.json'

        parsejson = ParseJson(url_data, path_of_file, user_address)

        my_sell_points: List[SellPoint] = parsejson.station_list()

        pdv: SellPoint

        # set current widget position and zoom
        self.map_widget.set_position(location[0], location[1])  # Domicile
        self.map_widget.set_zoom(13)
        #set_first_marker
        marker_1 = self.map_widget.set_position(location[0], location[1], marker=True, marker_color_circle = '#396D46', marker_color_outside = '#0C9F31', text_color = '#3F6990')
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
            text2 = str(pdv.address[0]) + ' ' + str(pdv.address[1]) + ' ' + str(pdv.address[2])
            text3 = ""
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
                    text5 = ""
                    text6 = ""
                    text7 = ""
                    for jour in range(0, 6):
                        jour_en_lettre = str(pdv.week_hours.day_hours[0][jour][0])
                        if pdv.week_hours.day_hours[0][jour][1]:
                            text5 += '\n' + jour_en_lettre + " pas d'horaire spécifiée"
                        else:
                            opening = pdv.week_hours.day_hours[0][jour][2][0]
                            closing = pdv.week_hours.day_hours[0][jour][2][1]
                            if opening.__len__() == 2:
                                text6 += '\n' + jour_en_lettre + " ouverture le matin de " + opening[0].replace('.', 'h') + " à " + opening[1].replace('.', 'h') + " et l'après midi' de " + closing[0].replace('.', 'h') + " à " + closing[1].replace('.', 'h')
                                
                            else:
                                text7 += '\n' + jour_en_lettre + " ouverture de " + opening.replace('.', 'h') + " à " + closing.replace('.', 'h')
                    print(text5)
                    print(text6)
                    print(text7)
            prices_txt: str = ""
            prices_txt_geo: str = ""
            print("\n")
            for price in pdv.prices:
                if price != []:
                    prices_txt += "\nCarburant " + str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\nDernière mise à jour du prix :" + "\n" + str(price[2]) + "\n"          
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
                new_marker = self.map_widget.set_marker(pdv.address[3], pdv.address[4], marker_color_circle = '#736A7C', marker_color_outside = '#8551BF', text=pdv.name + '\n' + prices_txt_geo + '\n', text_color = '#FF0000', image = ph, image_zoom_visibility=(15, float("inf")))
                #new_marker.hide_image(True)
            else:
                new_marker = self.map_widget.set_marker(pdv.address[3], pdv.address[4], text=pdv.name + '\n' + prices_txt_geo + '\n', text_color = '#3F6990', image = ph, image_zoom_visibility=(15, float("inf")))
                #new_marker.hide_image(True)

            i += 1

Main()