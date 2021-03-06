# pyManageContainers

pyManageContainers is a Python based command line script that reads a directory which has your Docker Compose files in yml format and generates a menu that lists each service (which is parsed from each compose file). After you select a service from a menu, you can then pick an action from a menu with 4 actions: Build, Stop,Stop & Delete,Recreate (delete and recreate).This script runs the docker-compose, docker start, docker stop,docker rm commands for you so you don't have type them out. It was tested on Linux but should work on Windows too,

### Setup

- Edit pyManageContainers.py and find the line `ymlDirectory="./"` and set it to the full path where your docker compose yml scripts are located. So for example `ymlDirectory="/home/devslash/compose"`on Linux or `ymlDirectory="C:\\Docker\\Compose\\"` The double slashes are important for Windows. The path must end in a slash.
- If you want to ignore any compose files, enter the file names into `ignoreFiles=[]` with each file name wrapped in double quotes and a comma separating each file name. Ex: `ignoreFiles=["portainer.yml","nextcloud.yml"]`
- Run the python script `python pyManageContainers.py`

You can also use command line parameters to run this script without any user input. The way you run it is with the name of the container and the menu # of the action. For example, you can recreate your container called Wordpress by running the command `python pyManageContainers.py Wordpress 4` where 4 is the action to take and corresponds to the number in the action selection.

You can also use `--all` parameter to perform an action on all containers. For example, to rebuild all containers, you can run `python pyManageContainers.py --all 4`

Please submit an issue if you run into any problems or would like to suggest new features. 
