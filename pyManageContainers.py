import glob
from operator import itemgetter
import os
import re
import sys

ignoreFiles = []; # Enter file names separated by a comma to specify compose files to ignore
ymlDirectory="./";

# Don't edit anything below this line
actions=['Build','Stop','Stop & Delete','Recreate'];

def buildContainer(container_index,container_action):
     global containers
   
     #print(container_index)
     #sys.exit()
 
     container = containers[container_index];

     if container_action == 1: # Build
          cmd="docker-compose -f " + container[1] + " up --no-start && docker start " + container[0];
             
          if len(container) > 2:
               cmd=cmd + " && docker start " + container[2];

          os.system(cmd);

          sys.exit(0);
     elif container_action == 2: # Stop
          cmd="docker stop " + container[0];

          if len(container) > 2:
               cmd=cmd + " && docker stop " + container[2];

          os.system(cmd);

          sys.exit(0);
     elif container_action == 3: # Stop & Delete
          cmd="docker stop " + container[0] + " && docker rm " + container[0];

          if len(container) > 2:
              cmd=cmd + " && docker stop " + container[2] + " && docker rm " + container[2];

          os.system(cmd);

          sys.exit(0);
     elif container_action == 4: # Recreate
          cmd="docker stop " + container[0] + " && docker rm " + container[0];
               
          if len(container) > 2:
               cmd=cmd + " && docker stop " + container[2] + " && docker rm " + container[2];

          os.system(cmd);

          cmd="docker-compose -f " + container[1] + " up --no-start && docker start " + container[0];
             
          if len(container) > 2:
               cmd=cmd + " && docker start " + container[2];

          os.system(cmd);

          sys.exit(0);
     elif container_action == 99:
          sys.exit();

def containerMenu(containers):
     while True:
          for i in range(len(containers)):
              print (str(i+1) + '. ' + containers[i][0]);

          print ("99. Exit");
          
          try:
               container_name=int(input("Please select a container: "));
          except:
               print("Invalid input");
 
          if container_name == 99:
               sys.exit();

          if container_name < 0 or container_name > len(containers):
               print("Invalid container selection");
          else:
               # Index is 0 based so subtract 1
               container_name=container_name-1;
                
               break;
     
     # get the action
     while True:
          for a in range(len(actions)):
               print (str(a+1) + '. ' + actions[a]);

          print ("99. Exit");

          try:
               container_action=input("Please select an action: ");
               container_action=int(container_action);
          except:
               print("Invalid input");
 
          if container_action == 99:
               sys.exit();

          if container_action < 0 or container_action > len(actions):
               print("Invalid action number");
          else:
               break;
        
     buildContainer(container_name,container_action);

def getContainers():
     global ignoreFiles
     global ymlDirectory

     containers = []; # Holds all compose files

     # Set the global delimiter
     delimiter=None;

     if sys.platform == "win32":
          delimiter = "\\";
     else:
          delimiter = "/";

     if ymlDirectory[-1] != delimiter:
          ymlDirectory=ymlDirectory + delimiter;

     files=glob.glob(ymlDirectory + "*.yml");

     if not files:
           print("No yml compose files found");
           sys.exit(0);

     # Loop through all yml files in the specified directory
     for currFile in files:
          if currFile.rfind(delimiter) != -1:
               fileWithoutPath=currFile[currFile.rfind(delimiter)+1:];
          else:
               fileWithoutPath=currFile;

          if fileWithoutPath in ignoreFiles:
               continue;

          myfile = open(currFile, "rt"); # Open current file for reading
          contents = myfile.read(); # read the entire file into a var 
          myfile.close();
     
          # Look for container name 
          matches = [];

          # Find all lines contianing container_name that do not start with a comment (#)
          matches=re.findall(r"([^#]container_name: [a-zA-Z0-9]\S+)",contents);
     
          # Some compose files define more than 1 container name. This script only reads up to 2 container_names
          if len(matches) == 1:
               containers.append((matches[0].replace("container_name: ","").strip(),currFile));
          elif len(matches) == 2:
               containers.append((matches[0].replace("container_name: ","").strip(),currFile,matches[1].replace("container_name: ","")));

     # Sort results by index 0
     containers=sorted(containers,key=itemgetter(0));

     return containers;
 
# Set working directory so docker-compose can find the .env if it is needed
os.chdir(ymlDirectory);

containers=getContainers();

container_name_index=-1;
container_action_index=-1;

# Get command line arguments
if len(sys.argv) > 1:
     try:
          container_action_index=int(sys.argv[2]);
          
          if container_action_index < 0 or container_action_index > len(actions):
               print("Invalid action number");
               sys.exit();
     except:
          print("The action is invalid");
          sys.exit();
         
     if sys.argv[1] != "--all":
          # Validate container name 
          for i in range(len(containers)):
               if containers[i][0].strip() == sys.argv[1]:
                    container_name_index=int(i);
                    break;
   
          if container_name_index == -1:
               print("Invalid container name");
               sys.exit();
     
          buildContainer(container_name_index,container_action_index);
     else:
          for container_index in range(len(containers)):
               buildContainer(container_index,container_action_index);
               
else:
     containerMenu(containers);
