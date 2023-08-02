from consts import *
from api import *
from helper import *
from inputHandling import *

def addToProject(newContent: str, dirLoc: str) -> None:
    existingFiles = getExistingFiles(dirLoc)
    existingFilesStr = ", ".join([f"'{f[:-3]}'" for f in existingFiles])
    
    fileEditContentPairs = getFCPairs(newContent, existingFilesStr)
    for fileName, newContent in fileEditContentPairs:
        fileLoc = os.path.join(dirLoc, fileName + ".md")
        if os.path.exists(fileLoc):
            with open(fileLoc, "r", encoding="utf-8") as f:
                oldContent = f.read()
            mergeContent(fileLoc, oldContent, newContent)
        else:
            saveMarkdownFile(fileLoc, newContent)
    
def getFCPairs(newContent: str, existingFilesStr: str) -> list[tuple[str, str]]:
    response = getGPTOutput(populateFindEditsPrompt(PROMPTTEXT_MERGECONTENT, newContent, existingFilesStr), MODEL_MAX_TOKENS)
    output = response["choices"][0]["message"]["content"]

    print(output)
    print("------------")

    return splitOutput(output)

def mergeContent(fileLoc: str, oldContent: str, newContent: str) -> str:
    response = getGPTOutput(populateMergeContentPrompt(PROMPTTEXT_MERGECONTENT, oldContent, newContent), MODEL_MAX_TOKENS)
    mergedContent = response["choices"][0]["message"]["content"]

    with open(fileLoc, "w", encoding="utf-8") as f:
        f.write(mergedContent)


if __name__ == "__main__":
    addToProject(loadInputFromTerminal(), input("Project dir location: "))






