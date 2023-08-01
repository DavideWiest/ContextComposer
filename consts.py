

NEWFILE_KW = "NEWFILE: "
INPUTYPE_OPTIONS = ["text", "t", "textFile", "tf", "audioFile", "af"]

MAX_SENTECE_WC = 25

WHISPER_API_MB_LIMIT = 25

GPT_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.1
MODEL_MAX_TOKENS = 4_000 # 97 tokens as margin of safety
MAX_OUTPUT_TOKENS = 2_0000
INPUT_TOKEN_SPLIT_COUNT = MODEL_MAX_TOKENS - MAX_OUTPUT_TOKENS

with open("generator_files/system_role.txt", "r") as f:
    SYSTEM_ROLE = f.read()
with open("generator_files/prompt.txt", "r") as f:
    PROMPTTEXT = f.read()

