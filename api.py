import os
import math
from collections import deque
import openai
from consts import *
from helper import *

openai.api_key = os.getenv("OPENAI_MAC_KEY")


def getTextFromAudioFile(audioFileLoc):
    raiseErrIfFileNotExists(audioFileLoc)

    transcriptFull = whisperCallSplit(split_mp3_into_parts(audioFileLoc))

    return transcriptFull

def whisperCallSplit(audioParts):
    transcriptFull = "\n".join(
        openai.Audio.transcribe("whisper-1", audioPart)["text"] for audioPart in audioParts
    )

    return transcriptFull

def getFullGPTOutput(input: str) -> list[tuple[str, str]]:
    "splits the text up into"

    filePairs = []

    rawPromptTokens = len(encoding.encode(PROMPTTEXT))
    ssbt = splitSentencesByTokens(input, INPUT_TOKEN_SPLIT_COUNT - rawPromptTokens)
    # print("ssbt")
    # print(ssbt)

    splitInput = deque(ssbt)
    # TODO: if not accurate enough, inlcude previous messages with a separate variable for that
    
    while splitInput:
        subinput = splitInput.pop()

        existingFiles = [fp[0] for fp in filePairs]
        existingFilesStr = ", ".join(existingFiles) + "\n\n"
        response = getGPTOutput(
            populatePrompt(PROMPTTEXT, subinput, existingFilesStr), MODEL_MAX_TOKENS
        )
        outputText = response["choices"][0]["message"]["content"]

        print("ot")
        print(outputText)
        print("----------")
        if response["choices"][0]["finish_reason"] != "stop":
            subinput_0, subinput_1 = splitSentencesByTokens(input, math.ceil(INPUT_TOKEN_SPLIT_COUNT / 2))
            splitInput.appendleft(0, subinput_0)
            splitInput.appendleft(1, subinput_1)
        else:
            filePairs += splitOutput(outputText)

    return filePairs


def rewriteAllFiles(outputDir):
    existing_files = []
    for filename in os.listdir(outputDir):
        file_path = os.path.join(outputDir, filename)
        if not os.path.isfile(file_path) or not filename.endswith(".md"): continue
        if filename.startswith(".") or ".obsidian" in filename or ".github" in filename: continue

        existing_files.append(file_path)
    
    for file_path in existing_files:
        with open(file_path, "r") as f:
            file = f.read()

        fileRewritten = getGPTOutput(
            populatePrompt(PROMPTTEXT, file, os.listdir(outputDir)), MODEL_MAX_TOKENS
        )
        fileRewritten = fileRewritten["choices"][0]["message"]["content"]

        with open(file_path, "w") as f:
            f.write(fileRewritten)


def getGPTOutput(prompt, maxTotalTokens, previous_messages = []):
    maxOutputTokens = maxTotalTokens - len(encoding.encode(prompt))
    return openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_ROLE
            },
        ]
         + previous_messages +
        [
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=maxOutputTokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

