

NEWSECTION_KW = "\n# "
INPUTYPE_OPTIONS = ["text", "t", "textFile", "tf", "audioFile", "af", "youtubeLink", "yl"]

MAX_SENTECE_WC = 25

WHISPER_API_MB_LIMIT = 25

GPT_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0
MODEL_MAX_TOKENS = 4_000 # 97 tokens as margin of safety
MAX_OUTPUT_TOKENS = 2_0000
INPUT_TOKEN_SPLIT_COUNT = MODEL_MAX_TOKENS - MAX_OUTPUT_TOKENS

with open("generator_files_en/system_role.txt", "r") as f:
    SYSTEM_ROLE = f.read()
with open("generator_files_en/prompt.txt", "r") as f:
    PROMPTTEXT = f.read()
with open("generator_files_en/prompt_rewrite.txt", "r") as f:
    PROMPTTEXT_REWRITE = f.read()
with open("generator_files_en/prompt_findeditfiles.txt", "r") as f:
    PROMPTTEXT_FINDEDITS = f.read()
with open("generator_files_en/prompt_mergecontent.txt", "r") as f:
    PROMPTTEXT_MERGECONTENT = f.read()