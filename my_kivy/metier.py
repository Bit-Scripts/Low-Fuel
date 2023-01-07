import platform
import random
import sys
import os

def random_coordonees():
    # random position
    Nord = 51.08916667
    Sud = 42.33277778
    Est = 8.23055556
    Ouest = -4.79555556
    random_latitude = random.uniform(Sud, Nord)
    random_longitude = random.uniform(Ouest, Est)
    return (random_latitude, random_longitude)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def tmp_dir():
    user_folder = os.path.expanduser("~")
    if platform.system() == 'Darwin':
        tmp_dir = user_folder + '/Library/Low-Fuel/'
    if platform.system() == 'Linux':
        tmp_dir = '/tmp/Low-Fuel/'
    if platform.system() == 'Windows':
        tmp_dir = user_folder + '\\AppData\\Local\\Temp\\Low-Fuel\\'
    return str(tmp_dir)