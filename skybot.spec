# -*- mode: python -*-

block_cipher = None

import sys
sys.setrecursionlimit(5000)

a = Analysis(['SkyBot.pyw'],
             pathex=['_dllFiles', 'D:\\SkyBot'],
             binaries=[],
             datas=[],
             hiddenimports=['talib.stream'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SkyBot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='skybot.ico')
