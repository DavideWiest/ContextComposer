from consts import *
from api import *
from helper import *
from inputHandling import *


def getFullGPTOutput(input: str) -> list[tuple[str, str]]:
    "splits the text up into"

    filePairs = []

    rawPromptTokens = len(encoding.encode(PROMPTTEXT))
    ssbt = splitSentencesByTokens(input, INPUT_TOKEN_SPLIT_COUNT - rawPromptTokens)
    # print("ssbt")
    # print(ssbt)

    splitInput = deque(ssbt)
    
    while splitInput:
        subinput = splitInput.pop()

        existingFiles = [fp[0] for fp in filePairs]
        existingFilesStr = ", ".join(existingFiles) + "\n\n"
        response = getGPTOutput(
            populatePrompt(PROMPTTEXT, subinput, existingFilesStr), MODEL_MAX_TOKENS
        )
        outputText = response["choices"][0]["message"]["content"]

        if response["choices"][0]["finish_reason"] != "stop":
            subinput_0, subinput_1 = splitSentencesByTokens(input, math.ceil(INPUT_TOKEN_SPLIT_COUNT / 2))
            splitInput.appendleft(0, subinput_0)
            splitInput.appendleft(1, subinput_1)
        else:
            filePairs += splitOutput(outputText)

    return filePairs


if __name__ == "__main__":
    outputDir = generateOutputDir()
    saveAllFiles(getFullGPTOutput(loadInputFromTerminal()), outputDir)
    rewriteAllFiles(outputDir)