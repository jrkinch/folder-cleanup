'''
    Created by jrkinch
    Tests the folder cleanup module.
    
    Run with:
        'python -m pytest -v' in the 'folder-cleanup' folder 
        project directory for default verbose output.


    TODO: Testing different pytest parameters for different output: 
            - like -v for more verbose info and using specified marked tests.
'''
import os
import shutil
import atexit
from src.cleanup.cleanup import Cleanup


if os.getcwd()[-5:] == 'tests': #using 'tests' folder
    homePath = os.path.dirname(os.getcwd())
else: #using script or running in 'folder-cleanup' folder.
    homePath = os.getcwd()

if not os.path.exists("test-run"):
    os.makedirs("test-run")

def copy_backups():
    """
        Copies the sample files and restores them.
    """
    shutil.copyfile(f"{homePath}/tests/test_files/backup_restore/sample_img.png",
    f"{homePath}/tests/test_files/sample_img.png")
    shutil.copyfile(f"{homePath}/tests/test_files/backup_restore/sample_doc.txt",
    f"{homePath}/tests/test_files/sample_doc.txt")
    shutil.copyfile(f"{homePath}/tests/test_files/backup_restore/sample_main.py",
    f"{homePath}/tests/test_files/sample_main.py")

class TestCleanup():
    """Tests for the cleanup module."""
    def setup_method(self,method):
        """
            Setting up class for each test case.
        """
        print(f"Setting up {method}")
        #pylint: disable=attribute-defined-outside-init
        #This use case defines variables for each test case before running.
        self.src = f"{os.getcwd()}/test-run"
        self.testing_files = f"{homePath}/tests/test_files"
        self.restore_files = f"{homePath}/tests/backup_restore"
        self.testing_folder = f"{self.src}/test"

        self.tidy = Cleanup(self.src,self.testing_folder)

    def teardown_method(self,method):
        """
            Tearing down after each test case.
        """
        print(f"Tearing down {method}")

    def test_validate_source_folder(self, capsys):
        """Check source folder to test 'validate_directory' function."""
        self.tidy.validate_directory(self.src)
        stdout = capsys.readouterr()

        assert f"Folder '{self.src}' already exists.\n" in stdout

    def test_validate_destination_folder_new(self, capsys):
        """Check new destination folder to test 'validate_directory' function."""
        self.tidy.validate_directory(self.testing_folder)
        stdout = capsys.readouterr()

        assert f"Folder '{self.testing_folder}' not found. Creating folder...\n" in stdout

    def test_validate_destination_folder_exists(self, capsys):
        """Check existing destination folder to test 'validate_directory' function."""
        self.tidy.validate_directory(self.testing_folder)
        stdout = capsys.readouterr()

        assert f"Folder '{self.testing_folder}' already exists.\n" in stdout

    def test_setup_sorting_folders_new(self, capsys):
        """Check new sorting folders to test 'setup_sorting_folders' function."""
        temp_string = ''
        self.tidy.setup_sorting_folders()
        stdout = capsys.readouterr()

        for folder in self.tidy.sort_to:
            #pylint: disable=line-too-long
            #This use case is fine as it already contains variables in a fstring.
            temp_string += f"Folder '{folder}' not found, creating {folder} in {self.testing_folder}.\n"

        assert temp_string in stdout

    def test_setup_sorting_folders_existing(self, capsys):
        """
            Check existing sorting folders to test 
            'setup_sorting_folders' function.
        """
        temp_string = ''
        self.tidy.setup_sorting_folders()
        stdout = capsys.readouterr()

        for folder in self.tidy.sort_to:
            temp_string += f"Folder '{folder}' already exists.\n"

        assert temp_string in stdout

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

    def test_move_newly_created_files(self):
        """
            Check fileList after dynamically created files 
            and moving to test 'move_file_item' function.
        """
        with open(f"{self.testing_files}/new_sample_doc.txt", "w", encoding='utf-8') as file:
            file.write("Hello World")
        with open(f"{self.testing_files}/new_sample_main.py", "w", encoding='utf-8') as file:
            file.write('print("Hello World")')

        file1, file2 = "new_sample_doc.txt", "new_sample_main.py"

        self.tidy.move_file_item(self.testing_files, self.src, file1)
        self.tidy.move_file_item(self.testing_files, self.src, file2)

        self.tidy.fileList = os.listdir(self.src)

        assert file1 in self.tidy.fileList
        assert file2 in self.tidy.fileList

    def test_move_test_files_existing(self):
        """
            Check fileList after existing file move 
            to test 'move_file_item' function.
        """
        copy_backups()

        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        ext1 = self.tidy.get_ext(file1)
        ext2 = self.tidy.get_ext(file2)
        ext3 = self.tidy.get_ext(file3)
        expected1 = f"{ext1[0]}_{self.tidy.current_time.strftime('%m-%d-%Y_%I_%M_%S_%p')}{ext1[1]}"
        expected2 = f"{ext2[0]}_{self.tidy.current_time.strftime('%m-%d-%Y_%I_%M_%S_%p')}{ext2[1]}"
        expected3 = f"{ext3[0]}_{self.tidy.current_time.strftime('%m-%d-%Y_%I_%M_%S_%p')}{ext3[1]}"

        self.tidy.move_file_item(self.testing_files, self.src, file1)
        self.tidy.move_file_item(self.testing_files, self.src, file2)
        self.tidy.move_file_item(self.testing_files, self.src, file3)

        self.tidy.fileList = os.listdir(self.src)

        assert expected1 in self.tidy.fileList
        assert expected2 in self.tidy.fileList
        assert expected3 in self.tidy.fileList

    def test_get_ext_func(self):
        """
            Tests the return values from the 'check_ext' function.
        """
        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        ext1 = self.tidy.get_ext(file1)
        ext2 = self.tidy.get_ext(file2)
        ext3 = self.tidy.get_ext(file3)

        assert ext1 == ('sample_img','.png')
        assert ext2 == ('sample_doc','.txt')
        assert ext3 == ('sample_main','.py')

    def test_sort_files_to_test_folder(self):
        """Check that files moved to the destination folder with 'sort_folder_contents' function."""
        file1, file2, file3 = "sample_img.png", "sample_doc.txt", "sample_main.py"
        ext1 = self.tidy.get_ext(file2)
        ext2 = self.tidy.get_ext(file3)
        expected1 = f"{ext1[0]}_{self.tidy.current_time.strftime('%m-%d-%Y_%I_%M_%S_%p')}{ext1[1]}"
        expected2 = f"{ext2[0]}_{self.tidy.current_time.strftime('%m-%d-%Y_%I_%M_%S_%p')}{ext2[1]}"

        self.tidy.sort_folder_contents()

        self.tidy.imageFileList = os.listdir(f"{self.testing_folder}/Images")
        self.tidy.docFileList = os.listdir(f"{self.testing_folder}/Documents")

        assert file1 in self.tidy.imageFileList
        assert file2 in self.tidy.docFileList
        assert file3 in self.tidy.docFileList
        assert expected1 in self.tidy.docFileList
        assert expected2 in self.tidy.docFileList

    @staticmethod
    def clean(): #pragma: no cover
    #this with atexit couldn't have .self variables, have to pass the full path
        """This is called after suite is finished running, copys the backup 
        files so test can run again and deletes the test destination folder from Desktop."""
        path = "./test-run"
        if os.path.exists(path):
            print("Test suite completed, exiting...")
            copy_backups()
            shutil.rmtree(path)

    atexit.register(clean) #pragma: no cover

if __name__ == '__main__': #pragma: no cover
    import subprocess

    #pylint: disable=undefined-variable
    #Using default cwd for current working directory.
    subprocess.check_call(["pytest", "-v"], cwd=cwd, check=False)
