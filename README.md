# pyManageContainers

pyManageContainers is a Python based command line script that reads a directory which has your Docker Compose files in yml format and generates a menu that lists each service (which is parsed from each compose file). After you select a service from a menu, you can then pick an action from a menu with 4 actions: Build, Stop,Stop & Delete,Recreate (delete and recreate).This script runs the docker-compose, docker start, docker stop,docker rm commands for you so you don't have type them out.

### Setup

- Edit pyManageContainers.py and edit the line `files=glob.glob("*.yml")` and set the full path to your yml files. So for example `files=glob.glob("/home/devslash/compose/*.yml")`
- If you want to ignore any compose files, enter the file names into `ignoreFiles=[]` with each file name wrapped in double quotes and a comma separating each file name. Ex: `ignoreFiles=["portainer.yml","nextcloud.yml"]`
- Run the python script `python pyManageContainers.py

Please submit an issue if you run into any problems or would like to suggest new features. 
