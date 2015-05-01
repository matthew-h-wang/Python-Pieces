from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())
# -*- mode: python -*-
a = Analysis(['C:\\Users\\Matthew\\Documents\\GitHub\\Python-Pieces\\4-23-package\\main.py'],
             pathex=['C:\\Users\\Matthew\\Documents\\GitHub\\Python-Pieces\\4-23-package'],
             hiddenimports=[],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PythonPieces.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='C:\\Users\\Matthew\\Documents\\GitHub\\Python-Pieces\\4-23-package\\icons\\PythonIco.ico')
coll = COLLECT(exe, Tree('./'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='PythonPieces')
