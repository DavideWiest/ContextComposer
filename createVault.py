from consts import *
from api import *
from helper import *
from inputHandling import *


def getFullLLMOutput(input: str, llmconsts: LLMConsts) -> list[tuple[str, str]]:
    "splits the text up into"

    if (input.strip() == ""):
        raise ValueError("Input string may not be empty. This is likely because your options did not allow for text to be extraced/loaded. Try again.")

    filePairs = []

    rawPromptTokens = len(encoding.encode(llmconsts.PROMPTTEXT))
    ssbt = splitSentencesByTokens(input, INPUT_TOKEN_SPLIT_COUNT - rawPromptTokens)
    # print("ssbt")
    # print(ssbt)

    splitInput = deque(ssbt)
    
    while splitInput:
        subinput = splitInput.pop()

        existingFiles = [fp[0] for fp in filePairs]
        existingFilesStr = ", ".join(existingFiles) + "\n\n"
        response = getGPTOutput(
            populatePrompt(llmconsts.PROMPTTEXT, subinput, existingFilesStr), MODEL_MAX_TOKENS
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
    generatorDir = validatedItemInputFromList("Generator files directory", getGeneratorDirOptions())
    llmconsts = LLMConsts(generatorDir)
    saveAllFiles(getFullLLMOutput(loadInputFromTerminal(), llmconsts), outputDir)
    rewriteAllFiles(outputDir, llmconsts)