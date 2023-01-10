# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
import sys
import os

if sys.getrecursionlimit() != None:
    sys.setrecursionlimit(sys.getrecursionlimit()*1000000)

block_cipher = None

ROOT_DIR = os.path.dirname(os.path.abspath("__file__")) # This is your Project Root

a = Analysis(
    [
        'main.py',
    ],
    pathex=[ROOT_DIR],
    binaries=[],
    datas=[('image\\Logo_Bit-Scripts.gif', 'image\\'),
        ('image\\petrol_pump.ico', 'image\\'),
        ('petrol_pump.png','.\\'),
        ('image\\marker.png', 'kivy_garden\\mapview\\icons\\'),
        ('domain\\data.py', 'domain\\data.py'),
        ('domain\\logic.py', 'domain\\logic.py'),
        ('domain\\user.py', 'domain\\user.py'),
        ('my_kivy\\color_kivy.py', 'my_kivy\\color_kivy.py'),
        ('my_kivy\\logic_uix.py', 'my_kivy\\logic_uix.py'),
        ('my_kivy\\metier.py', 'my_kivy\\metier.py'),
        ('my_kivy\\my_widgets.py', 'my_kivy\\my_widgets.py'),
        ('my_kivy\\ui_object.py', 'my_kivy\\ui_object.py'),
        ('my_kivy\\logic_uix.py', 'my_kivy\\logic_uix.py'), 
        ('parsedata\\parse_json.py', 'parsedata\\parse_json.py'),
    ],
    hiddenimports=['kivy_garden', 'mapview'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    [],
    name='Low-Fuel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='%TEMP%',
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['image\\petrol_pump.ico'],
)
