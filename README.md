<h1>folder-cleanup</h1>
Project to organize specified folder.<br><br>

Takes two arguments, source path and destination path.<br>
&emsp;- Source path is file location to get organized.<br>
&emsp;- Destination path is where to move the files to.<br>
&emsp;- Both arguments can be the same if organized folders are preferred at same location.<br>

> [!NOTE]
> Folders after cleanup completes:<br>
> 'Documents', 'Folders', 'Images', 'Programs', 'Shortcuts', 'Sounds', 'ZIP', 'Videos'


<h2>Installation:</h2>
1) Run <code>pip install -r docs/requirements.txt</code> in the project folder or 'run_requirements.bat' from the 'scripts' folder.
	

<h2>Getting Started:</h2>
Steps:<br>
1) Put the 'cleanup.py' file in any project.<br>
2) Use <code>from cleanup import Cleanup</code> in project.<br>
&emsp;- can also use <code>from cleanup.cleanup import Cleanup</code> if using the 'cleanup' folder.<br>
3) Init the class with source and destination paths and then use the 'run_cleanup' function from module.<br>
- Example:<br>
<code>tidy = Cleanup(source,destination)
tidy.run_cleanup()
</code>

> [!NOTE]
> Running <code>python main.py</code> from the src folder organizes the 'Downloads' folder and Desktop.<br>


<h2>Testing:</h2>
1) Run <code>python -m pytest -v</code> in the project folder or 'run_test.bat' file from the 'scripts' folder.<br>
