# -*- mode: python ; coding: utf-8 -*-
#from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks, get_deps_minimal
from PyInstaller.utils.hooks import collect_data_files
import sys

datas = [('image/Logo_Bit-Scripts.png', 'image')]
datas += collect_data_files('kivy_garden')

block_cipher = None

version_python = f'{sys.version[0]}.{sys.version_info[1]}'

if version_python == '3.10':
    kivy_garden = '/opt/homebrew/lib/python3.10/site-packages/kivy_garden/mapview'    
    pathex=['/opt/homebrew/lib/python3.10/site-packages/']
    target_arch='arm64'
else :
    if version_python == '3.9':
        kivy_garden = '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/kivy_garden/mapview'
        pathex=['/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/']    
        target_arch='x86_64'

name=f'Low-Fuel_{target_arch}.app'

datas = [
    ('image/Logo_Bit-Scripts.gif', 'image'),
    ('%s/icons/cluster.png' % kivy_garden,'kivy_garden/mapview/icons'),
    ('%s/icons/marker.png' % kivy_garden,'kivy_garden/mapview/icons')
]
datas += collect_data_files('kivy_garden', 'mapview')

a = Analysis(
    [
        'main.py', 
        'domain/data.py', 
        'domain/logic.py', 
        'domain/user.py', 
        'my_kivy/coloredlabel.py', 
        'my_kivy/create_uix.py', 
        'parsedata/parse_json.py', 
    ],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=['kivy_garden', 'mapview'],
    hookspath=[],#hookspath(),
    hooksconfig={},
    runtime_hooks=[],#runtime_hooks(),
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    #**get_deps_all(),
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='lowfuel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=target_arch,
    codesign_identity=None,
    entitlements_file=None,
    icon=['image/petrol_pump.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lowfuel',
)
app = BUNDLE(
    coll,
    name=name,
    icon='image/petrol_pump.icns',
    bundle_identifier='com.lowfuel.bitscripts',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'Privacy - Documents Folder Usage Description': "This application requests access to the user's Documents folder.",
        'NSDocumentsFolderUsageDescription': "This application requests access to the user's Documents folder.",
        'Application is background only': False,
        'AllowCacheDelete': True,
        'AllowPersonalCaching': True,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeIconFile': 'petrol_pump.icns',
                'LSItemContentTypes': ['com.lowfuel.bitscripts'],
                'LSHandlerRank': 'Owner'
            }
        ]
    },
)

