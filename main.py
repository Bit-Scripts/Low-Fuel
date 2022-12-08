from typing import Union
from geopy import Nominatim
from parsedata.parse_xml import ParseXml
from domain.user import AddressUser
from domain.data import SellPoint
# Formulaire

locator = Nominatim(user_agent="low-fuel")

url_data = 'https://donnees.roulez-eco.fr/opendata/instantane'
path_of_file = 'info.gouv/PrixCarburants_instantane'

user_address = AddressUser(1, '1-3 Rue des Minimes',  '37000', 'Tours', 5)

client_address = user_address.street + ' ' + user_address.post_code + ' ' + user_address.city
location = locator.geocode(client_address)

user_address = AddressUser(1, '29 BOULEVARD DE DIJON',  '10800', 'Saint-Julien-les-Villas', 2, location.latitude, location.longitude)


sell_points : list(SellPoint) = ParseXml(url_data, path_of_file, user_address)

for sell_point in sell_points: 
    print(str(sell_point.id) + '\n' + sell_point.name + '\n' + sell_point.address + '\n' + str(sell_point.week_hours) + '\n' + str(sell_point.prices) + '\n' + str(sell_point.services))
