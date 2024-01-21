
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

        changedFiles = ["components/test.c"]
        pushHash = "UNKNOWN"
        pushUser = "UNKNOWN"
        today = date.today()
        pushDate = today.strftime("%B %d, %Y")
        
    
    for changedFilePath in changedFiles:

        # If a GitHub Actions file was changed, we shouldn't update it
        if (not changedFilePath.startswith(".github")):

            # Step 1: For each file, open it with "read" first and retrieve all contents.
            # - Look for any #define or #include statemenets and mark their locations. This is so that, later,
            #   we know where to best append the version info.
            changedFileContents = []
            index = 0
            lastHeaderIndex = -1
            firstDefineIndex = -1
            versionInfoIndex = -1
            with open(changedFilePath, "r") as changedFile:

                for line in changedFile:
                    changedFileContents.append(line)
                    if (versionInfoIndex == -1 and line.startswith("#define VERSION_INFORMATION")):
                        versionInfoIndex = index
                    elif (line.startswith("#include")):
                        lastHeaderIndex = index
                    elif (firstDefineIndex == -1 and line.startswith("#define")):
                        firstDefineIndex = index
                    index += 1
            a=1
            # Step 2: append info back into file
            # Rules:
            # - if exists a "#define VERSION_INFORMATION", replace it with the new one
            # - if currently no version information constants, put it above the first #define (anything)
            # - if no #defines anywhere, put it behind the last #include
            # - if no #includes (ain't no way), put it at the start of file
            print("Writing to file: " + changedFilePath)
            with open(changedFilePath, "w") as changedFile:
                infoString = "#define VERSION_INFORMATION \"Push HashCode: " + pushHash + ", by: " + pushUser + ", on: " + pushDate + ".\"\n"

                if (versionInfoIndex != -1):
                    insertLineToFile(changedFile, changedFileContents, infoString, versionInfoIndex, True)
                elif (firstDefineIndex != -1):
                    insertLineToFile(changedFile, changedFileContents, infoString, firstDefineIndex)
                elif (lastHeaderIndex != -1):
                    insertLineToFile(changedFile, changedFileContents, infoString, lastHeaderIndex + 1)
                else:
                    insertLineToFile(changedFile, changedFileContents, infoString, 0)

                print("  - appended: " + infoString)
