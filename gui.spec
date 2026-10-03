# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for RimWorld Modlist Manager GUI

This spec file ensures all dependencies are bundled correctly.
Run: pyinstaller gui.spec
"""

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    # CRITICAL: DearPyGui and other modules that PyInstaller can't auto-detect
    hiddenimports=[
        'dearpygui',
        'dearpygui.dearpygui',
        'dearpygui._dearpygui',
        'requests',
        'bs4',
        'beautifulsoup4',
        'urllib3',
        'charset_normalizer',
        'tkinter',
        'tkinter.filedialog',
        'config',
        'main',
        'moulinette',
        'steam_workshop',
        'mod_utils',
        'utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
