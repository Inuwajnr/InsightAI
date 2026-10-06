# -*- mode: python ; coding: utf-8 -*-

import os

project_dir = os.path.dirname(os.path.abspath(SPEC))

icon_file = os.path.join(
    project_dir,
    "assets",
    "insightai.ico"
)

logo_file = os.path.join(
    project_dir,
    "assets",
    "insightai_logo.png"
)

a = Analysis(
    ['main.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[
        (icon_file, 'assets'),
        (logo_file, 'assets'),
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='InsightAI Offline',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[icon_file],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InsightAI Offline',
)