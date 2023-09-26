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

def rewriteAllFiles(outputDir, llmconsts: LLMConsts):
    existing_files = []
    for filename in os.listdir(outputDir):
        file_path = os.path.join(outputDir, filename)
        if not os.path.isfile(file_path) or not filename.endswith(".md"): continue
        if filename.startswith(".") or ".obsidian" in filename or ".github" in filename: continue

        existing_files.append(file_path.replace(".md", ""))
    
    for file_path in existing_files:
        with open(file_path, "r") as f:
            file = f.read()

        fileRewritten = getGPTOutput(
            populatePrompt(llmconsts.PROMPTTEXT_REWRITE, file, os.listdir(outputDir)), MODEL_MAX_TOKENS, llmconsts
        )
        fileRewritten = fileRewritten["choices"][0]["message"]["content"]

        with open(file_path, "w") as f:
            f.write(fileRewritten)


def getGPTOutput(prompt, maxTotalTokens, llmconsts: LLMConsts, previous_messages = []):
    maxOutputTokens = maxTotalTokens - len(encoding.encode(prompt))
    return openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": llmconsts.SYSTEM_ROLE
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

