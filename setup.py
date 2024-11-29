from setuptools import setup

OPTIONS = {
    'argv_emulation':False,

}

setup(
    app=["main-mac.py"],
    setup_requires=["py2app"],
)