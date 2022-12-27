# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'domain/data.py', 'domain/logic.py', 'domain/user.py', 'my_kivy/coloredlabel.py', 'my_kivy/create_uix.py', 'parsedata/parse_json.py'],
    pathex=[],
    binaries=[],
    datas=[('image/Logo_Bit-Scripts.gif','image'),('image/marker.png','kivy_garden/mapview/icons')],
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
    target_arch='arm64',
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
    name='Low-Fuel.app',
    icon='image/petrol_pump.icns',
    bundle_identifier=None,
)
