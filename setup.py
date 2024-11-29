import os
from setuptools import setup

OPTIONS = {
    'argv_emulation': False,
    'iconfile': os.path.abspath('./iconmac.icns'),  # Use absolute path
}

setup(
    app=["main-mac.py"],               # Your main script
    options={"py2app": OPTIONS},       # Pass OPTIONS dictionary to py2app
    setup_requires=["py2app"],         # py2app setup requirement
)
