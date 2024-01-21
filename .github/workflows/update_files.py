
import os

from datetime import date

def insertLineToFile(file, originalContent, line, lineNumber, doReplace=False):
    for i in range(0,len(originalContent)):
        if (i == lineNumber):
            file.write(line)
            if not doReplace:
                file.write(originalContent[i])
        else:
            file.write(originalContent[i])

if __name__ == "__main__":
    try:
        # Set up environment variables, retrieved from GitHub Actions
        # The get_changed_files GitHub tool outputs a string of file paths separated by spaces
        changedFiles = os.environ["CHANGED_FILES"].split(" ") 
        # changedFiles = ["components/ecu/ecu_firmware/Core/Src/can.c"]
        # The hashcode of this push
        pushHash = os.environ["GITHUB_SHA"] 
        # The person who triggered the push
        pushUser = os.environ["GITHUB_ACTOR"]
        # Quality of life: today's date :D
        today = date.today()
        pushDate = today.strftime("%B %d, %Y")
    except Exception as e:
        print("ERROR: failed to retrieve GitHub environment variables. Stopping version information insertion. \n" + 
              "- Make sure that files were changed and there are no spaces in file names (required by the module this action uses)\n" +
              "- If this still doesn't work, shit.\n" + 
              "Python error message: ", end = "")
        print(e)

        # This is a debug tool:
        # changedFiles = [".github/workflows/test.c"]
        # pushHash = "GITHUB_SHA"
        # pushUser = "GITHUB_ACTOR"
        # today = date.today()
        # pushDate = today.strftime("%B %d, %Y")
        
    
    for changedFilePath in changedFiles:

        # For each file, open it with "read" first and retrieve all contents.
        # After, we'll open it with "write" to copy everything plus the version info back
        changedFileContents = []
        index = 0
        firstHeaderIndex = -1
        firstDefineIndex = -1
        versionInfoIndex = -1
        with open(changedFilePath, "r") as changedFile:

            for line in changedFile:
                changedFileContents.append(line)
                if (firstHeaderIndex == -1 and line.startswith("#include")):
                    firstHeaderIndex = index
                if (firstDefineIndex == -1 and line.startswith("#define")):
                    firstDefineIndex = index
                if (versionInfoIndex == -1 and line.startswith("#define VERSION_INFORMATION")):
                    versionInfoIndex = index
                index += 1
        
        print("Writing to file: " + changedFilePath)
        with open(changedFilePath, "w") as changedFile:
            infoString = "#define VERSION_INFORMATION \"Push HashCode: " + pushHash + ", by: " + pushUser + ", on: " + pushDate + ".\"\n"

            if (versionInfoIndex != -1):
                insertLineToFile(changedFile, changedFileContents, infoString, versionInfoIndex, True)
            elif (firstDefineIndex != -1):
                insertLineToFile(changedFile, changedFileContents, infoString, firstDefineIndex)
            elif (firstHeaderIndex != -1):
                insertLineToFile(changedFile, changedFileContents, infoString, firstHeaderIndex)
            else:
                insertLineToFile(changedFile, changedFileContents, infoString, 0)

            print("  - appended: " + infoString)
