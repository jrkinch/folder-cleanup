<h1>folder-cleanup</h1>
Project to organize specified folder.<br><br>

<h2>Description:</h2>

Allows user to organize files into different extension type folders.<br>

Creating an instance of the class takes two arguments, source path and destination path.<br>
&emsp;- Source path is file location to get organized.<br>
&emsp;- Destination path is where to move the files to.<br>
&emsp;- Both arguments can be the same if organized folders are preferred at same location.<br>

> [!NOTE]
> Folders after cleanup completes:<br>
> 'Documents', 'Folders', 'Images', 'Programs', 'Shortcuts', 'Sounds', 'ZIP', 'Videos'

<h2>Getting Started:</h2>

<h3>Installation:</h3>
1. Clone the repo:

```console
git clone https://github.com/jrkinch/folder-cleanup.git
```

<br>
2. Install python dependencies:

```console
pip install -r docs/requirements.txt
```
> [!TIP]
> Can also run the 'run_requirements.bat' from the 'scripts' folder.

<h3>Usage:</h3>
Steps to use in own project:<br>
1) Put the 'cleanup.py' file in any project.<br>
&emsp;- can also put the 'cleanup' folder from the 'src' folder into project.<br>
2) Use <code>from cleanup import Cleanup</code> in project.<br>
&emsp;- can also use <code>from cleanup.cleanup import Cleanup</code> if using the 'cleanup' folder from the 'src' folder.<br>
3) Init the class with source and destination paths and then use the 'run_cleanup' function from module.<br>
- Example using 'cleanup' folder:<br>

```python
from cleanup.cleanup import Cleanup
	
tidy = Cleanup(source,destination)
tidy.run_cleanup()
```

> [!NOTE]
> Running <code>python main.py</code> from the 'src' folder organizes the 'Downloads' folder and Desktop.<br>
> ```python
>python main.py
> ```



<h3>Testing:</h3>
1) Run tests from the project folder:<br>

```python
python -m pytest -v
```
> [!TIP]
> Can also run the 'run_test.bat' file from the 'scripts' folder..

<h2>Docker:</h2>
1) Builds the images and runs the containers for this project:<br>

```console
docker compose up
```
<br>
2) Stops and removes the containers for this project:<br>

```console
docker compose down
```
> [!NOTE]
> An image for the 'src/main' and 'tests' are created and those containers are ran when using docker compose.<br>
> Similiar to running <code>python main.py</code> and <code>python -m pytest -v</code> when using docker compose.
