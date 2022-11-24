import wget
from datetime import datetime,timedelta
import zipfile
import os
import xml.dom.minidom

filePath = 'info.gouv/PrixCarburants_instantane.zip'

if os.path.exists(filePath):
    os.remove(filePath)

url = 'https://donnees.roulez-eco.fr/opendata/instantane'

filename = wget.download(url, 'info.gouv/PrixCarburants_instantane.zip')

if (filename == 'info.gouv/PrixCarburants_instantane.zip'):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('info.gouv/')
        doc = xml.dom.minidom.parse('info.gouv/PrixCarburants_instantane.xml')
        print (doc)
        