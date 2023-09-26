from consts import *
from api import *
from helper import *
from inputHandling import *

from youtube_transcript_api import YouTubeTranscriptApi


def loadTranscriptYoutube(youtubeLink) -> str:
    return normalizeTranscript(YouTubeTranscriptApi.get_transcript(extractVideoId(youtubeLink)))

def normalizeTranscript(text: str) -> str:
    return text.replace("\n\n", "\n")

def extractVideoId(youtubeLinkOrId: str) -> str:
    if "youtube." not in youtubeLinkOrId and "youtu.be" not in youtubeLinkOrId: return youtubeLinkOrId

    if "youtube." in youtubeLinkOrId: return youtubeLinkOrId.split("v=")[-1].split("&")[0]
    return youtubeLinkOrId.split("/")[-1].split("&")[0]