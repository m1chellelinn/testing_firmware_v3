import os

from datetime import date



if __name__ == "__main__":
    try:
        # Set up environment variables, retrieved from GitHub Actions
        # The get_changed_files GitHub tool outputs a string of file paths separated by spaces
        changedFiles = os.environ["CHANGED_FILES"].split(" ") 
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
        changedFiles = []
    
    for changedFilePath in changedFiles:

        # For each file, open it with "read" first and retrieve all contents.
        # After, we'll open it with "write" to copy everything plus the version info back
        changedFileContents = []
        with open(changedFilePath, "r") as changedFile:

            for line in changedFile:
                changedFileContents.append(line)
            
        with open(changedFilePath, "w") as changedFile:

            for line in changedFileContents:
                changedFile.write(line)

            changedFile.write("#define VERSION_INFORMATION \"" + pushHash + " by " + pushUser + " on " + pushDate + "\"")
