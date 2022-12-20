# -*- mode: python ; coding: utf-8 -*-
#from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
import sys

sys.setrecursionlimit(sys.getrecursionlimit()*5)

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('domain','domain'),('my_kivy','my_kivy'),('parsedata','parsedata')],
    datas=[('image','image'),('info.gouv','info.gouv'),('image/marker.png', 'kivy_garden/mapview/icons/')],
    hiddenimports=[],
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
 #   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    [],
    name='Low-Fuel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='/tmp',
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['image/petrol_pump.png'],
)
