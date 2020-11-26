# pyManageContainers

pyManageContainers is a Python based script that reads a directory which has your Docker Compose files and generates a menu for each service (which is parsed from each compose file).

### Setup

- Edit the line `files=glob.glob("*.yml")` and set the full path to your yml so for example `files=glob.glob("/home/devslash/compose/*.yml")`
- If you want to ignore any compose files, enter the file names into `ignoreFiles=[]` with each file name wrapped in double quotes and a comma separating each file name.
- Run the python script `python pyManageContainers.py

Please submit an issue if you run into any problems or would like to suggest new features. 
