'''
    Created by jrkinch
    Tests the folder cleanup module.
    
    Run with:
        'python -m pytest -v' in the 'cleanupProject' folder project directory for default verbose output.
        'python -m pytest -m <marked> -v' in the 'cleanupProject' folder project directory for specific function test.
            setup_existing: tests both directories for the 'validate_directory' and the destination path for the 'setup_sorting_folders' functions with existing folder
			setup_new: tests both directories for the 'validate_directory' and the destination path for the 'setup_sorting_folders' functions with creating new folders
			move_files: tests the 'move_file_item' function
			cls_misc_func: tests the 'get_ext' function
			sort: tests the 'sort_folder_contents' function

    TODO: Testing different pytest parameters for different output: 
            - like -v for more more verbose info and using specified marked tests.
            
    Folders after cleanup completes:
    ['Documents', 'Folders', 'Images', 'Programs', 'Shortcuts', 'Sounds', 'ZIP']
'''
import pytest
import os
import shutil
import atexit
from cleanup.cleanup import Cleanup

#set variable depending where pytest tests are ran, variable not able to be set with __name__ == '__main__' section. Sets 'homePath' to 'cleanupProject' folder.
if os.getcwd()[-5:] == 'tests': #using 'tests' folder
    homePath = os.path.dirname(os.getcwd())
else: #using script or running in 'cleanupProject' folder.
    homePath = os.getcwd()


def copy_backups():
    shutil.copyfile(f"{homePath}\\tests\\test_files\\backup_restore\\sample_img.png",f"{homePath}\\tests\\test_files\\sample_img.png")
    shutil.copyfile(f"{homePath}\\tests\\test_files\\backup_restore\\sample_doc.txt",f"{homePath}\\tests\\test_files\\sample_doc.txt")
    shutil.copyfile(f"{homePath}\\tests\\test_files\\backup_restore\\sample_main.py",f"{homePath}\\tests\\test_files\\sample_main.py")

class TestCleanup():

    def setup_method(self,method):
        print(f"Setting up {method}")
        
        self.src = f"{os.environ['USERPROFILE']}\\OneDrive\\Desktop"
        self.testing_files = f"{homePath}\\tests\\test_files"
        self.restore_files = f"{homePath}\\tests\\backup_restore"
        self.testing_folder = f"{self.src}\\test"
        
        self.tidy = Cleanup(self.src,self.testing_folder)
   
    def teardown_method(self,method):
        print(f"Tearing down {method}")
    
    @pytest.mark.setup_existing
    def test_validate_source_folder(self, capsys):
        """Check source folder to test 'validate_directory' function."""
        self.tidy.validate_directory(self.src)
        stdout, stderr = capsys.readouterr()
        
        assert stdout == f"Folder '{self.src}' already exists.\n"

    @pytest.mark.setup_new
    def test_validate_destination_folder_new(self, capsys):
        """Check new destination folder to test 'validate_directory' function."""
        self.tidy.validate_directory(self.testing_folder)
        stdout, stderr = capsys.readouterr()
        
        assert stdout == f"Folder '{self.testing_folder}' not found. Creating folder...\n"       

    @pytest.mark.setup_existing
    def test_validate_destination_folder_exists(self, capsys):
        """Check existing destination folder to test 'validate_directory' function."""
        self.tidy.validate_directory(self.testing_folder)
        stdout, stderr = capsys.readouterr()
        
        assert stdout == f"Folder '{self.testing_folder}' already exists.\n"             
    
    @pytest.mark.setup_new
    def test_setup_sorting_folders_new(self, capsys):
        """Check new sorting folders to test 'setup_sorting_folders' function."""
        temp_string = ''
        self.tidy.setup_sorting_folders()
        stdout, stderr = capsys.readouterr()
        
        for folder in self.tidy.sortTo:
            temp_string += f"Folder '{folder}' not found, creating {folder} in {self.testing_folder}.\n"
        
        assert stdout == temp_string

    @pytest.mark.setup_existing
    def test_setup_sorting_folders_existing(self, capsys):
        """Check existing sorting folders to test 'setup_sorting_folders' function."""
        temp_string = ''
        self.tidy.setup_sorting_folders()
        stdout, stderr = capsys.readouterr()
        
        for folder in self.tidy.sortTo:
            temp_string += f"Folder '{folder}' already exists.\n"
            
        assert stdout == temp_string  
    
    @pytest.mark.move_files
    def test_move_test_files_new(self):
        """Check fileList after new file move to test 'move_file_item' function."""
        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        
        self.tidy.move_file_item(self.testing_files, self.src, file1)
        self.tidy.move_file_item(self.testing_files, self.src, file2)
        self.tidy.move_file_item(self.testing_files, self.src, file3)
        
        self.tidy.fileList = os.listdir(self.src)
        
        assert file1 in self.tidy.fileList
        assert file2 in self.tidy.fileList
        assert file3 in self.tidy.fileList
    
    @pytest.mark.move_files
    def test_move_newly_created_files(self):
        """Check fileList after dynamically created files and moving to test 'move_file_item' function."""
        with open(f"{self.testing_files}\\new_sample_doc.txt", "w") as file:
            file.write("Hello World")
        with open(f"{self.testing_files}\\new_sample_main.py", "w") as file:
            file.write('print("Hello World")')
    
        file1, file2 = "new_sample_doc.txt", "new_sample_main.py"
       
        self.tidy.move_file_item(self.testing_files, self.src, file1)
        self.tidy.move_file_item(self.testing_files, self.src, file2)
        
        self.tidy.fileList = os.listdir(self.src)
        
        assert file1 in self.tidy.fileList
        assert file2 in self.tidy.fileList
        
    @pytest.mark.move_files    
    def test_move_test_files_existing(self):
        """Check fileList after existing file move to test 'move_file_item' function."""
        copy_backups()
        
        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        ext1 = self.tidy.get_ext(file1)
        ext2 = self.tidy.get_ext(file2)
        ext3 = self.tidy.get_ext(file3)
        expected1 = f"{ext1[0]}_{self.tidy.currentTime.strftime("%m-%d-%Y_%I_%M_%S_%p")}{ext1[1]}"
        expected2 = f"{ext2[0]}_{self.tidy.currentTime.strftime("%m-%d-%Y_%I_%M_%S_%p")}{ext2[1]}"
        expected3 = f"{ext3[0]}_{self.tidy.currentTime.strftime("%m-%d-%Y_%I_%M_%S_%p")}{ext3[1]}"
                
        self.tidy.move_file_item(self.testing_files, self.src, file1)
        self.tidy.move_file_item(self.testing_files, self.src, file2)
        self.tidy.move_file_item(self.testing_files, self.src, file3)
        
        self.tidy.fileList = os.listdir(self.src)
        
        assert expected1 in self.tidy.fileList
        assert expected2 in self.tidy.fileList
        assert expected3 in self.tidy.fileList
    
    @pytest.mark.cls_misc_func
    def test_get_ext_func(self):
        """Check misc class 'get_ext' function."""
        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        ext1 = self.tidy.get_ext(file1)
        ext2 = self.tidy.get_ext(file2)
        ext3 = self.tidy.get_ext(file3)
        
        assert ext1 == ('sample_img','.png')
        assert ext2 == ('sample_doc','.txt')
        assert ext3 == ('sample_main','.py')
    
    @pytest.mark.sort
    def test_sort_files_to_test_folder(self):
        """Check that files moved to the destination folder with 'sort_folder_contents' function."""
        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        ext1 = self.tidy.get_ext(file2)
        ext2 = self.tidy.get_ext(file3) 
        expected1 = f"{ext1[0]}_{self.tidy.currentTime.strftime("%m-%d-%Y_%I_%M_%S_%p")}{ext1[1]}"
        expected2 = f"{ext2[0]}_{self.tidy.currentTime.strftime("%m-%d-%Y_%I_%M_%S_%p")}{ext2[1]}"
        
        self.tidy.sort_folder_contents()
        
        self.tidy.imageFileList = os.listdir(f"{self.testing_folder}\\Images")
        self.tidy.docFileList = os.listdir(f"{self.testing_folder}\\Documents")
        
        assert file1 in self.tidy.imageFileList
        assert file2 in self.tidy.docFileList
        assert file3 in self.tidy.docFileList
        assert expected1 in self.tidy.docFileList
        assert expected2 in self.tidy.docFileList
    
    
    def clean(): #this with atexit couldn't have .self variables, have to pass the full path
        """This is called after suite is finished running, copys the backup files so test can run again and deletes the test destination folder from Desktop."""
        path = f"{os.environ['USERPROFILE']}\\OneDrive\\Desktop\\test"
        if os.path.exists(path):
            print("Test suite completed, exiting...")
            copy_backups()
            shutil.rmtree(path)
        
    atexit.register(clean)

   
if __name__ == '__main__':    
    import subprocess
    
    subprocess.run("python -m pytest -v")    