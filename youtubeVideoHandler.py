from helper import *

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptList


def loadTranscriptYoutube(ytVideoId: str, youtubeTranscriptLanguage: str) -> str:
    return extractTranscriptText(YouTubeTranscriptApi.get_transcript(ytVideoId, languages=[youtubeTranscriptLanguage]))

def normalizeTranscript(text: str) -> str:
    return text.replace("\n\n", "\n")

def extractTranscriptText(transcriptResponse: list[dict]):
    return "\n".join([item["text"] for item in transcriptResponse])

def extractVideoId(youtubeLinkOrId: str) -> str:
    if "youtube." not in youtubeLinkOrId and "youtu.be" not in youtubeLinkOrId: return youtubeLinkOrId

    if "youtube." in youtubeLinkOrId: return youtubeLinkOrId.split("v=")[-1].split("&")[0]
    return youtubeLinkOrId.split("/")[-1].split("&")[0]

def getAvailableTranscripts(ytVideoId: str) -> list:
    return [i.language_code for i in YouTubeTranscriptApi.list_transcripts(ytVideoId)]

def getTranscript(textinput: str) -> str:
    ytVideoId = extractVideoId(textinput)
    availabletranscripts = getAvailableTranscripts(ytVideoId)
    print(availabletranscripts)
    youtubeTranscriptLanguage = validatedItemInputFromList("Transcript language: ", availabletranscripts)
    return loadTranscriptYoutube(ytVideoId, youtubeTranscriptLanguage)