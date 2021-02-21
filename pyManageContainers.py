import glob
from operator import itemgetter
import os
import re
import sys

if len(sys.argv) == 3: 
     container_name=sys.argv[1]
     
     try:
          container_action=int(sys.argv[2])
     except:
          print("The action is invalid")
          sys.exit()
else:
     container_name=""
     container_action=0

ignoreFiles = [] # Enter file names separated by a comma to specify compose files to ignore
ymlDirectory="./"

# Don't edit anything below this line
files=glob.glob(ymlDirectory + "*.yml")

containers = [] # Holds all compose files 
delimiter=None

# Set the global delimiter
if sys.platform == "win32":
     delimiter = "\\"
else:
     delimiter = "/"

if not files:
    print("No yml compose files found")
    sys.exit(0)

# Loop through all yml files in the specified directory
for currFile in files:
     if currFile.rfind(delimiter) != -1:
          fileWithoutPath=currFile[currFile.rfind(delimiter)+1:]
     else:
          fileWithoutPath=currFile

     if fileWithoutPath in ignoreFiles:
          continue

     myfile = open(currFile, "rt") # Open current file for reading
     contents = myfile.read() # read the entire file into a var 
     myfile.close() 
     
     # Look for container name 
     matches = []

     # Find all lines contianing container_name that do not start with a comment (#)
     matches=re.findall(r"([^#]container_name: [a-zA-Z0-9]\S+)",contents)
     
     # Some compose files define more than 1 container name. This script only reads up to 2 container_names
     if len(matches) == 1:
         containers.append((matches[0].replace("container_name: ",""),currFile))
     elif len(matches) == 2:
         containers.append((matches[0].replace("container_name: ",""),currFile,matches[1].replace("container_name: ","")))

# Sort results by index 0
containers=sorted(containers,key=itemgetter(0))
actions=['Build','Stop','Stop & Delete','Recreate']
 
# Set working directory so docker-compose can find the .env if it is needed
os.chdir(ymlDirectory)

def menu():
     container_response = -1
     container_num=-1;
     
     if container_name == "":
          while container_response != 99:
               for i in range(len(containers)):
                    print (str(i+1) + '. ' + containers[i][0])

               print ("99. Exit")
          
               container_response=0

               container_response=int(input("Please select a container: "))

               if container_response == 99:
                    sys.exit()

               # Index is 0 based so subtract 1
               container_response=container_response-1
                
               break
     else: # container name was provided as a cmd line param
          for i in range(len(containers)):
               if containers[i][0].strip() == container_name:
                    container_response=i;
                    break
          
          if container_response == -1:
               print("Invalid container name");
               sys.exit()
     
     # get the action
     if container_action == 0:
          for a in range(len(actions)):
               print (str(a+1) + '. ' + actions[a])

               print ("99. Exit")

               action_response=int(input("Please select an action: "))
     else:
          if container_action < 0 or container_action > len(actions):
               print("Invalid action number")
               sys.exit()
         
          action_response=container_action

     # Start the build
     if action_response == 1: # Build
          cmd="docker-compose -f " + containers[container_response][1] + " up --no-start && docker start " + containers[container_response][0]
             
          if len(containers[container_response]) > 2:
               cmd=cmd + " && docker start " + containers[container_response][2]

          os.system(cmd)

          sys.exit(0)
     elif action_response == 2: # Stop
          cmd="docker stop " + containers[container_response][0]

          if len(containers[container_response]) > 2:
               cmd=cmd + " && docker stop " + containers[container_response][2]

          os.system(cmd)

          sys.exit(0)
     elif action_response == 3: # Stop & Delete
          cmd="docker stop " + containers[container_response][0] + " && docker rm " + containers[container_response][0]

          if len(containers[container_response]) > 2:
              cmd=cmd + " && docker stop " + containers[container_response][2] + " && docker rm " + containers[container_response][2]

          os.system(cmd)

          sys.exit(0)
     elif action_response == 4: # Recreate
          cmd="docker stop " + containers[container_response][0] + " && docker rm " + containers[container_response][0]
               
          if len(containers[container_response]) > 2:
               cmd=cmd + " && docker stop " + containers[container_response][2] + " && docker rm " + containers[container_response][2]

          os.system(cmd)

          cmd="docker-compose -f " + containers[container_response][1] + " up --no-start && docker start " + containers[container_response][0]
             
          if len(containers[container_response]) > 2:
               cmd=cmd + " && docker start " + containers[container_response][2]

          os.system(cmd)

          sys.exit(0)
     elif action_response == 99:
          sys.exit()
 
menu()
