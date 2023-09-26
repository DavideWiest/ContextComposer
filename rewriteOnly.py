import colorama
from consts import *
from api import *
from helper import *
from inputHandling import *

colorama.init()
Fore = colorama.Fore

generatorDir = validatedItemInputFromList("Generator files directory", getGeneratorDirOptions())
llmconsts = LLMConsts(generatorDir)

rewriteAllFiles(input("Dir to rewrite files in: "), llmconsts)