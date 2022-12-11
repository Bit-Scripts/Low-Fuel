from typing import List
from geopy import Nominatim
from parsedata.parse_json import ParseJson
from domain.user import AddressUser
from domain.data import SellPoint
from domain.logic import address_to_coord
# Formulaire

locator = Nominatim(user_agent="low-fuel")

url_data : str = 'https://www.data.gouv.fr/fr/datasets/r/b3393fc7-1bee-42fb-a351-d7aedf5d5ff0'
path_of_file : str = 'info.gouv/prix-carburants.json'

user_address = AddressUser(1, '1-3 Rue des Minimes',  '37000', 'Tours', 5)

location = address_to_coord(user_address.street + ' ' + user_address.post_code + ' ' + user_address.city) 


user_address = AddressUser(1, '1-3 Rue des Minimes',  '37000', 'Tours', 5, location[0],location[1])

my_sell_points: List[SellPoint] = ParseJson (url_data, path_of_file, user_address).station_list()

pdv: SellPoint

for pdv in my_sell_points:
    print('\n')
    print("------------------------------------------------------------")
    print(pdv.idSP + '\n')
    print(pdv.name + '\n')
    print(pdv.address + '\n')
    print(str(pdv.week_hours) + '\n')
    print(str(pdv.prices) + '\n')
    print(str(pdv.services) + '\n')
    print(str(round(pdv.distance,2)).replace('.', ',') + ' km \n')
    print("------------------------------------------------------------")