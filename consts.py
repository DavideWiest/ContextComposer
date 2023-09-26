

NEWSECTION_KW = "\n# "
INPUTYPE_OPTIONS = ["text", "t", "textFile", "tf", "audioFile", "af", "youtubeVideo", "yt"]

MAX_SENTECE_WC = 25

WHISPER_API_MB_LIMIT = 25

GPT_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0
MODEL_MAX_TOKENS = 4_000 # 97 tokens as margin of safety
MAX_OUTPUT_TOKENS = 2_0000
INPUT_TOKEN_SPLIT_COUNT = MODEL_MAX_TOKENS - MAX_OUTPUT_TOKENS

class LLMConsts:
    def __init__(self, generatorDir):
        with open(f"{generatorDir}/system_role.txt", "r") as f:
            self.SYSTEM_ROLE = f.read()
        with open(f"{generatorDir}/prompt.txt", "r") as f:
            self.PROMPTTEXT = f.read()
        with open(f"{generatorDir}/prompt_rewrite.txt", "r") as f:
            self.PROMPTTEXT_REWRITE = f.read()
        with open(f"{generatorDir}/prompt_findeditfiles.txt", "r") as f:
            self.PROMPTTEXT_FINDEDITS = f.read()
        with open(f"{generatorDir}/prompt_mergecontent.txt", "r") as f:
            self.PROMPTTEXT_MERGECONTENT = f.read()
