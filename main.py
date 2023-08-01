import colorama
from consts import *
from api import *
from helper import *
from inputHandling import *

colorama.init()
Fore = colorama.Fore


if __name__ == "__main__":
    outputDir = generateOutputDir()
    saveAllFiles(getFullGPTOutput(loadInputFromTerminal()), outputDir)
    rewriteAllFiles(outputDir)