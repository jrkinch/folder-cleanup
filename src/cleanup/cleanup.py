'''
    Created by jrkinch
    Project to organize specified folder.
    Takes two arguments, source path and destination path. 
        - Source path is file location to get organize.
        - Destination path is where to move the files to.
        - Both arguments can be the same if organized folders are preferred at same location.
    
    TODO: Testing modularity, add more file extensions
'''
import os
import shutil
import datetime
import platformdirs

class Cleanup():
    """
        Class to organize specified folder.
        
        Takes two arguments, source path and destination path. 
        - Source path is file location to get organize.
        - Destination path is where to move the files to.
        - Both arguments can be the same if organized folders are preferred at same location.
    """
    #pylint: disable=too-many-instance-attributes.
    #Using 12 in this case since types and folders are used.
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.paths = [source, destination]
        self.current_time = datetime.datetime.now() #used for duplicate named files.
        self.sort_to = ['Folders','Documents','Images',
        'Programs','Sounds','ZIP','Shortcuts', 'Videos']
        self.doc_types = ['.pdf','.docx','.txt','.html','.java','.py']
        self.image_types = ['.png','.jpg','.fon','.ttf','.ico']
        self.program_types = ['.exe','.msi','.apk','.jar','.bat']
        self.sound_types = ['.midi','.wav','.aup3']
        self.zip_types = ['.zip','.7z','.def']
        self.shortcut_types = ['.url','.lnk']
        self.video_types = ['.mp4','.mov','.avi','.mpeg']

    def validate_directory(self, folder):
        """
            This validates the specified folder exists or creates one.
        """
        if not os.path.exists(f"{folder}"):
            print(f"Folder '{folder}' not found. Creating folder...")
            os.mkdir(f"{folder}")
        else:
            print(f"Folder '{folder}' already exists.")

    def check_directories(self):
        """
            This checks that the specified source and 
            destination paths are valid.
        """
        for folder in self.paths:
            self.validate_directory(folder)

    def setup_sorting_folders(self):
        """
            This validates the sorting folders exists or creates them.
        """
        for folder in self.sort_to:
            if not os.path.exists(f"{self.destination}/{folder}"):
                print(f"Folder '{folder}' not found, creating {folder} in {self.destination}.")
                os.mkdir(f"{self.destination}/{folder}")
            else:
                print(f"Folder '{folder}' already exists.")

    def move_file(self, source, destination):
        """
            This moves the specified file but uses 'shutil.copy2' 
            and 'os.remove' to copy then delete file to fix the 
            'invalid cross-device link' error with 'os.rename' 
            while using docker.
        """
        try:
            shutil.copy2(source, destination)
        except (FileNotFoundError, PermissionError, OSError, IsADirectoryError) as e:
            print(f"Unable to move file: {e}")

        try:
            os.remove(source)
        except (FileNotFoundError, PermissionError, OSError, IsADirectoryError) as e:
            print(f"Unable to delete file: {e}")

    def check_file_exists(self, destination_path):
        """
            This checks if the file is in the folder already. 
            Using shutil copy/copy2 doesn't throw the 'FileExistsError' 
            like the 'os.rename' function. 'shutil.SameFileError' 
            exception also doesn't seem to be caught. This function 
            is needed when using the new 'move_file' function with docker.
        """
        return os.path.exists(destination_path)

    def create_new_destination_file(self, source, destination, file):
        """
            This creates new file name with date and time for a duplicated file.
        """
        new_file_name = self.get_ext(file)
        #pylint: disable=line-too-long.
        #docker causes 'unterminated string literal' error when broken up for pylint.
        new_destination_path = os.path.join(destination,f"{new_file_name[0]}_{self.current_time.strftime('%m-%d-%Y_%I_%M_%S_%p')}{new_file_name[1]}")
        self.move_file(source, new_destination_path)

    def move_file_item(self, source, destination, file):
        """
            This moves the specified file from the source 
            folder to the destination folder.
        """
        source_path = os.path.join(source, file)
        destination_path = os.path.join(destination, file)
        if self.check_file_exists(destination_path):
            try:
                self.create_new_destination_file(source_path, destination, file)
            except (FileNotFoundError, PermissionError, OSError, IsADirectoryError) as e:
                print(f"An error has occurred: {e}")
        else:
            try:
                self.move_file(source_path, destination_path)
            except (FileNotFoundError, PermissionError, OSError, IsADirectoryError) as e:
                print(f"An error has occurred: {e}")

    def get_ext(self,file):
        """
            Separate the file name and file type extension.
        """
        return os.path.splitext(file)

    def sort_folder_contents(self):
        """
            This orgainzes the files based by the file types 
            variables tothe specified 'sort_to' folders.
        """
        file_list = os.listdir(self.source)
        for file in file_list:
            #gets and moves folders.
            if os.path.isdir(f"{self.source}/{file}") and \
                file not in self.sort_to and \
                file not in self.destination:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[0]}", file)
            #gets and moves the documents.
            elif self.get_ext(file)[1].lower() in self.doc_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[1]}", file)
            #gets and moves the images.
            elif self.get_ext(file)[1].lower() in self.image_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[2]}", file)
            #gets and moves the programs.
            elif self.get_ext(file)[1].lower() in self.program_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[3]}", file)
            #gets and moves the sounds.
            elif self.get_ext(file)[1].lower() in self.sound_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[4]}", file)
            #gets and moves the compression zips.
            elif self.get_ext(file)[1].lower() in self.zip_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[5]}", file)
            #gets and moves the shortcuts.
            elif self.get_ext(file)[1].lower() in self.shortcut_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[6]}", file)
            #gets and moves the videos.
            elif self.get_ext(file)[1].lower() in self.video_types:
                self.move_file_item(self.source, f"{self.destination}/{self.sort_to[7]}", file)

    def run_cleanup(self):
        """
            This runs entire process by first checking directory is
            valid, creating the sorting folders, then moving files to
            the sorting folders.
        """
        self.check_directories()
        self.setup_sorting_folders()
        self.sort_folder_contents()

#Testing module.
if __name__ == '__main__':
    #Looks at Desktop folder and orgainzes the files on the Desktop.
    SRC = platformdirs.user_desktop_dir()
    TEMP_SRC = f"{platformdirs.user_desktop_dir()}/test"

    tidy = Cleanup(SRC,SRC)
    tidy.run_cleanup()
