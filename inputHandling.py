from consts import *
from api import *
from helper import *
from youtubeVideoHandler import loadTranscriptYoutube, getAvailableTranscripts, extractVideoId

import os

def loadInputFromTerminal() -> str:
    inputType = validatedItemInputFromList("Input Type", INPUTYPE_OPTIONS).lower()

    if inputType in ("text", "t"):
        text = input("Text: ")
    elif inputType in ("textfile", "tf"):
        fileLoc = input("Text file location: ")
        text = loadTextFile(fileLoc)
    elif inputType in ("audiofile", "af"):
        text = aggregateText(getTextFromAudioFile, "Recording", "Next audio file path", True)
    elif inputType in ("youtubeVideo", "yt"):
        text = aggregateText(getTranscript, "Transcript", "Next Youtube Link or Video ID")
    else:
        raise Exception("Invalid input type")
    
    return text

def aggregateText(aggregationFunction: callable, textItemTitle: str, inputQuery: str, includeInputInItemTitle=False, requireFirst=True):
    text = ""
    textinput = ""
    i = 0 

    while textinput != "q":
            loadedText = aggregationFunction(textinput)
            text += f"{textItemTitle} {textinput if includeInputInItemTitle else ''} {i} \n\n"
            text += loadedText + "\n\n"

            textinput = input(f"{inputQuery} (q to quit): ")
            i+=1

def getTranscript(textinput: str) -> str:
    ytVideoId = extractVideoId(textinput)
    youtubeTranscriptLanguage = validatedItemInputFromList("Transcript language: ", getAvailableTranscripts())
    return loadTranscriptYoutube(ytVideoId, youtubeTranscriptLanguage)

def validatedItemInputFromList(inputTitle: str, inputs: list):
    print(f"{inputTitle}")
    print("\n".join(f" - {i}: {item}" for i, item in enumerate(inputs)))

    try:
        selectedIndex = int(input(f"Select an item (0-{len(inputs)-1}): "))
        if (selectedIndex < 0 or selectedIndex >= len(inputs)): 
            raise ValueError()
    except ValueError:
        print("Invalid input, try again")
        return validatedItemInputFromList(inputTitle, inputs)
    
    
    return inputs[selectedIndex]

def getGeneratorDirOptions() -> list[str]:
    return [item for item in os.listdir(os.getcwd()) if os.path.isdir(item) and item.startswith("generator_files")]