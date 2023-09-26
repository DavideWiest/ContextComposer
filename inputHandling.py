from consts import *
from api import *
from helper import *
from youtubeVideoHandler import getTranscript

import os

def loadInputFromTerminal() -> str:
    inputType = validatedItemInputFromList("Input Type", INPUTYPE_OPTIONS).lower()

    if inputType in ("text", "t"):
        text = input("Text: ")
    elif inputType in ("textfile", "tf"):
        fileLoc = input("Text file location: ")
        text = loadTextFile(fileLoc)
    elif inputType in ("audiofile", "af"):
        text = aggregateText(getTextFromAudioFile, "Recording", "Áudio file path", True)
    elif inputType in ("youtubeVideo", "yt"):
        text = aggregateText(getTranscript, "Transcript", "Youtube Link or Video ID")
    else:
        raise Exception("Invalid input type")
    

    print("--- Inputting finished. Please wait for the LLM to generate the output. ---")
    
    return text

def aggregateText(aggregationFunction: callable, textItemTitle: str, inputQuery: str, includeInputInItemTitle=False, requireFirst=True):
    text = ""
    textinput = ""
    i = 0 

    textinput = input(f"Initial: {inputQuery} (q to quit): ")

    while textinput != "q":
            loadedText = aggregationFunction(textinput)
            text += f"{textItemTitle} {textinput if includeInputInItemTitle else ''} {i} \n\n"
            text += loadedText + "\n\n"

            textinput = input(f"Next: {inputQuery} (q to quit): ")
            i+=1

    return text

def getGeneratorDirOptions() -> list[str]:
    return [item for item in os.listdir(os.getcwd()) if os.path.isdir(item) and item.startswith("generator_files")]