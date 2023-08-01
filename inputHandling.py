from consts import *
from api import *
from helper import *

def loadInputFromTerminal() -> str:
    inputType = input(f"Input Type ({', '.join(INPUTYPE_OPTIONS)})" + ": ").lower()

    if inputType in ("text", "t"):
        text = input("Text: ")
    elif inputType in ("textfile", "tf"):
        fileLoc = input("Text file location: ")
        text = loadTextFile(fileLoc)
    elif inputType in ("audiofile", "af"):
        fileLoc = input("Audio file location: ")
        text = getTextFromAudioFile(fileLoc)
    else:
        raise Exception("Invalid input type")
    
    return text
