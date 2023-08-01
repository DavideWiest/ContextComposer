import colorama
from consts import *
from api import *
from helper import *
from inputHandling import *

colorama.init()
Fore = colorama.Fore

rewriteAllFiles(input("Dir to rewrite files in: "))