import os
import io
import re
from datetime import datetime
from pydub import AudioSegment
from consts import *

import tiktoken

# Train a BPE tokeniser on a small amount of text
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
# Visualise how the GPT-4 encoder encodes text
encoding.encode("hello world aaaaaaaaaaaa")

def populatePrompt(prompt: str, text: str, existingFilesStr: str) -> str:
    return prompt \
        .replace("{text}", text) \
        .replace("{files}", ", ".join(existingFilesStr))

def raiseErrIfFileNotExists(fileLoc: str) -> str:
    if not os.path.exists(fileLoc): raise Exception("File does not exist")

def loadTextFile(fileLoc: str) -> str:
    raiseErrIfFileNotExists(fileLoc)
    with open(fileLoc, "r", encoding="utf-8") as f:
        return f.read()

def splitSentencesByTokens(text: str, token_split_count: int):
    sentences = splitTextBySentences(text, MAX_SENTECE_WC)
    sentenceTokens = [len(encoding.encode(sentence)) for sentence in sentences]

    currentSentenceBatch = ""
    textPieces = []
    currentBatchTokens = 0

    for i, s in enumerate(sentences):
        if currentBatchTokens + sentenceTokens[i] < token_split_count:
            textPieces.append(currentSentenceBatch)
            currentSentenceBatch = ""
            currentBatchTokens = 0
        
        currentSentenceBatch += " " + s
        currentBatchTokens += sentenceTokens[i]

    if currentSentenceBatch != "":
        textPieces.append(currentSentenceBatch)    

    return textPieces
    

def splitTextBySentences(text, max_sentence_wc):
    def split_long_sentence(sentence):
        if len(sentence.split()) <= max_sentence_wc:
            return [sentence]

        middle_comma_index = len(sentence) // 2
        while middle_comma_index < len(sentence) and sentence[middle_comma_index] != ',':
            middle_comma_index += 1

        return [sentence[:middle_comma_index], sentence[middle_comma_index + 1:]]

    sentences = [sentence.strip() for sentence in re.split(r'[.;]', text)]
    result = []
    for sentence in sentences:
        result.extend(split_long_sentence(sentence))

    return [sentence.strip() + "." for sentence in result if sentence.strip() != ""]

def split_mp3_into_parts(audioFileLoc: str, part_size_mb: int):
    # Convert bytes in-memory MP3 data to an AudioSegment object
    audio_segment = AudioSegment.from_file(io.BytesIO(open(audioFileLoc, "rb")), format='mp3')

    # Calculate the target size in bytes for each part
    target_size_bytes = part_size_mb * 1024 * 1024

    # Split the audio into parts
    parts = []
    num_parts = len(audio_segment) // target_size_bytes
    for i in range(num_parts):
        start_time = i * target_size_bytes
        end_time = (i + 1) * target_size_bytes
        part = audio_segment[start_time:end_time]
        parts.append(part)

    # Add the last part (if any) with the remaining audio
    if len(audio_segment) % target_size_bytes != 0:
        last_part = audio_segment[num_parts * target_size_bytes:]
        parts.append(last_part)

    return parts

def splitOutput(output: str) -> list[tuple[str, str]]:
    outputFilePairs = [
        (fileString.split("\n", 1)[0].strip(), fileString.split("\n", 1)[-1].strip()) for fileString in output.split(NEWFILE_KW) if fileString.strip() not in ("", "---")
    ]

    for i, fp in enumerate(outputFilePairs):
        if fp[1].strip().startswith("---"):
            outputFilePairs[i] = fp.strip()[3:]
        if fp[1].strip().endswith("---"):
            outputFilePairs[i] = fp.strip()[:-3]

    return outputFilePairs

def saveAllFiles(fileTuples: list[tuple[str, str]], outputDir):
    for name, content in fileTuples:
        fileLoc = outputDir + "/" + name + (".md" if not name.endswith(".md") else "")
        saveMarkdownFile(fileLoc, content)

def generateOutputDir():
    return "output/" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def saveMarkdownFile(file_path: str, content: str) -> None:
    # Create the necessary directories if they don't exist
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the file with the provided content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

