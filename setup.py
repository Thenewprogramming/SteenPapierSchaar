from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    windows = [{'script': "stPaSc_wxgame.py"}],
    zipfile = None,
)