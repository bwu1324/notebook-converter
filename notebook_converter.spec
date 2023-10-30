# -*- mode: python ; coding: utf-8 -*-


merge_nb_a = Analysis(
    ['merge_nb.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['notebook'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
merge_nb_pyz = PYZ(merge_nb_a.pure)

merge_nb_exe = EXE(
    merge_nb_pyz,
    merge_nb_a.scripts,
    [],
    exclude_binaries=True,
    name='merge_nb',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

nb2pdf_a = Analysis(
    ['nb2pdf.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['notebook'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
nb2pdf_pyz = PYZ(nb2pdf_a.pure)

nb2pdf_exe = EXE(
    nb2pdf_pyz,
    nb2pdf_a.scripts,
    [],
    exclude_binaries=True,
    name='nb2pdf',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    merge_nb_exe,
    merge_nb_a.binaries,
    merge_nb_a.datas,
    nb2pdf_exe,
    nb2pdf_a.binaries,
    nb2pdf_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='notebook-converter',
)
