# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for VespaFinder GUI application.

Build standalone executable:
    uv run pyinstaller vespa_finder.spec

Or use the build script:
    ./build_exe.sh
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Paths
block_cipher = None
project_root = os.path.abspath(os.path.dirname(SPEC))
src_path = os.path.join(project_root, 'src')

# Collect all vespa_finder submodules
hiddenimports = collect_submodules('vespa_finder')
hiddenimports += [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'folium',
    'folium.plugins',
    'jinja2',
    'branca',
    'certifi',
]

# Data files to include
datas = [
    # Include translations and other package data
    (os.path.join(src_path, 'vespa_finder', 'translations.py'), 'vespa_finder'),
]

# Add folium templates
try:
    datas += collect_data_files('folium')
    datas += collect_data_files('branca')
except Exception:
    pass

a = Analysis(
    ['gui.py'],  # Main entry point
    pathex=[src_path, project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
    ],
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
    [],
    name='VespaFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for CLI version
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'assets/icon.ico'
)

# For macOS, create an app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='VespaFinder.app',
        icon=None,  # Add icon path here: 'assets/icon.icns'
        bundle_identifier='com.vespafinder.app',
        info_plist={
            'CFBundleName': 'VespaFinder',
            'CFBundleDisplayName': 'VespaFinder',
            'CFBundleVersion': '0.3.0',
            'CFBundleShortVersionString': '0.3.0',
            'NSHighResolutionCapable': True,
        },
    )
