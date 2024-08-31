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

            
#Testing module.
if __name__ == '__main__':
    
    #This looks at my Download folder and organizes into folders in the same Downloads folder.
    src = f"{os.environ['USERPROFILE']}\\Downloads"
    tidy = Cleanup(src,src)
    tidy.run_cleanup()
    
    #Same behavior as above but with Desktop files.
    src = f"{os.environ['USERPROFILE']}\\OneDrive\\Desktop"
    tidy = Cleanup(src,src)
    tidy.run_cleanup()
   