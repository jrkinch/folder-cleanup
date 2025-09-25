'''
    Created by jrkinch
    Project to organize specified folder.
    Takes two arguments, source path and destination path. 
        - Source path is file location to get organize.
        - Destination path is where to move the files to.
        - Both arguments can be the same if organized folders are preferred at same location.
'''
import os
from cleanup.cleanup import Cleanup

if __name__ == '__main__':
    #This looks at my Download folder and organizes into folders in the same Downloads folder.
    DOWNLOAD_SRC = f"{os.environ['USERPROFILE']}\\Downloads"
    tidy = Cleanup(DOWNLOAD_SRC, DOWNLOAD_SRC)
    tidy.run_cleanup()

    #Same behavior as above but with Desktop files.
    DESKTOP_SRC = f"{os.environ['USERPROFILE']}\\OneDrive\\Desktop"
    tidy = Cleanup(DESKTOP_SRC, DESKTOP_SRC)
    tidy.run_cleanup()
