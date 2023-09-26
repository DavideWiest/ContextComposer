from consts import *
from api import *
from helper import *
from texthandler import loadTranscriptYoutube

import os

def loadInputFromTerminal() -> str:
    inputType = validatedItemInputFromList("Input Type", INPUTYPE_OPTIONS).lower()
    generatorDir = validatedItemInputFromList("Generator files directory", getGeneratorDirOptions())

    if inputType in ("text", "t"):
        text = input("Text: ")
    elif inputType in ("textfile", "tf"):
        fileLoc = input("Text file location: ")
        text = loadTextFile(fileLoc)
    elif inputType in ("audiofile", "af"):
        fileLoc = input("Audio file location: ")
        text = getTextFromAudioFile(fileLoc)
    elif inputType in ("youtubeLink", "yl"):
        youtubeLink = input("Youtube Link or Video ID: ")
        text = loadTranscriptYoutube(youtubeLink)
    else:
        raise Exception("Invalid input type")
    
    return text

def validatedItemInputFromList(inputTitle: str, inputs: list):
    print(f"{inputTitle}")
    print("\n".join(f" - {i}: {item}" for i, item in enumerate(inputs)))

    selectedIndex = input(f"Select an item (0-{len(inputs)-1})")

    if (selectedIndex < 0 or selectedIndex >= len(inputs)): 
        print("Invalid input, try again")
        return validatedItemInputFromList(inputTitle, inputs)
    
    return selectedIndex

def getGeneratorDirOptions() -> list[str]:
    return [item for item in os.listdir(os.getcwd()) if os.path.isdir(item) and item.startswith("generator_files")]