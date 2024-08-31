'''
    Created by jrkinch
    Project to organize specified folder.
    Takes two arguments, source path and destination path. 
        - Source path is file location to get organize.
        - Destination path is where to move the files to.
        - Both arguments can be the same if organized folders are preferred at same location.
    
    TODO: Testing modularity, add more file extensions
'''
import os,datetime

class Cleanup():
    def __init__(self,source,destination):
        self.source = source
        self.destination = destination
        self.paths = [source, destination]
        self.currentTime = datetime.datetime.now() #used for duplicate named files.
        self.sortTo = ['Folders','Documents','Images','Programs','Sounds','ZIP','Shortcuts']
        self.docTypes = ['.pdf','.docx','.txt','.html','.java','.py']
        self.imageTypes = ['.png','.jpg','.fon','.ttf','.ico']
        self.programTypes = ['.exe','.msi','.apk','.jar','.bat']
        self.soundTypes = ['.midi','.wav','.aup3']
        self.zipTypes = ['.zip','.7z','.def']
        self.shortcutTypes = ['.url','.lnk']        
        
    def validate_directory(self, folder):
        if not os.path.exists(f"{folder}"):
            print(f"Folder '{folder}' not found. Creating folder...")
            os.mkdir(f"{folder}")
        else:
            print(f"Folder '{folder}' already exists.")

    def check_directories(self):
        for folder in self.paths:
            self.validate_directory(folder)
        
    def setup_sorting_folders(self):
        for folder in self.sortTo:
            if not os.path.exists(f"{self.destination}\\{folder}"):
                print(f"Folder '{folder}' not found, creating {folder} in {self.destination}.")
                os.mkdir(f"{self.destination}\\{folder}")
            else:
                print(f"Folder '{folder}' already exists.")

    def move_file_item(self,source,destination,file):
        sourcePath = os.path.join(source,file)
        destinationPath = os.path.join(destination,file)
        try:
            os.rename(sourcePath,destinationPath)
        except FileExistsError: 
            newFileName = self.get_ext(file)
            newDestinationPath = os.path.join(destination,f"{newFileName[0]}_{self.currentTime.strftime("%m-%d-%Y_%I_%M_%S_%p")}{newFileName[1]}")
            os.rename(sourcePath,newDestinationPath)
        except PermissionError as e:
            print(f"Error with the '{self.destination}' folder: {e}") 

    def get_ext(self,file):
        return os.path.splitext(file)    
        
    def sort_folder_contents(self):
        self.fileList = os.listdir(self.source)
        for file in self.fileList:
            #gets and moves folders.
            if os.path.isdir(f"{self.source}\\{file}") and file not in self.sortTo and file not in self.destination:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[0]}", file)
            #gets and moves the documents.
            elif self.get_ext(file)[1].lower() in self.docTypes:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[1]}", file) 
            #gets and moves the images.
            elif self.get_ext(file)[1].lower() in self.imageTypes:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[2]}", file)
            #gets and moves the programs.
            elif self.get_ext(file)[1].lower() in self.programTypes:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[3]}", file)
            #gets and moves the sounds.
            elif self.get_ext(file)[1].lower() in self.soundTypes:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[4]}", file)
            #gets and moves the compression zips.
            elif self.get_ext(file)[1].lower() in self.zipTypes:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[5]}", file)
            #gets and moves the shortcuts.                
            elif self.get_ext(file)[1].lower() in self.shortcutTypes:
                self.move_file_item(self.source,f"{self.destination}\\{self.sortTo[6]}", file) 

    def run_cleanup(self):
        self.check_directories()
        self.setup_sorting_folders()
        self.sort_folder_contents()
        
#Testing module.
if __name__ == '__main__':
    
    #Looks at Desktop folder and orgainzes the files on the Desktop.
    src = f"{os.environ['USERPROFILE']}\\OneDrive\\Desktop"
    temp_src = f"{os.environ['USERPROFILE']}\\OneDrive\\Desktop\\test"
    
    tidy = Cleanup(src,src)
    tidy.run_cleanup()
    
