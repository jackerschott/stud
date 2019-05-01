#!/usr/bin/python3
import json
import os
import requests
import servers.theo4 as theo4
import servers.pap as pap
import servers.pt as pt
import signal
import sys
from getpass import getpass
from os import path
from studModule import StudModule, Lecture, PracticalCourse
from sys import exit

# Allow keyboard interrupt
signal.signal(signal.SIGINT, lambda x,y: { print(), sys.exit(0) })

# Load configurations
homePath = path.expanduser('~')
configDirPath = path.join(homePath, '.config', 'stud')
configFilePath = path.join(configDirPath, 'studrc.json')
moduleUrlsPath = path.join(configDirPath, 'moduleUrls.json')
ptCookiePath = path.join(configDirPath, 'pt_cjar')

with open(configFilePath) as configFile:
  config = json.load(configFile)
with open(moduleUrlsPath) as moduleUrlsFile:
  lecUrls = json.load(moduleUrlsFile)

studPath = config['studPath']
lecPath = path.join(studPath, config['lecFolderName'])
pcPath = path.join(studPath, config['pcFolderName'])

def ptCreateSession(session):
  # Login or use old session
  pt.loadSession(session, ptCookiePath)
  if not pt.checkForSavedSession(ptCookiePath) or not pt.checkLoginStatusPT(session):
    # Get username and password
    id = input("username for '" + pt.serverUrl + "': ")
    passw = getpass("password for '" + pt.serverUrl + "': ")
    print()

    # Login
    session, success = pt.loginPT(session, id, passw)
    if not success:
      print('Invalid username or password', file=sys.stderr)
      exit(-1)
    pt.saveSession(session, ptCookiePath)

# Check for module
if len(sys.argv) <= 1:
  print('You must specify a module', file=sys.stderr)
  exit(-1)

# Build module
moduleName = sys.argv[1]
if moduleName in config['lecs']:
  
  # Create and check for module folder
  folderPath = path.join(lecPath, config[moduleName + "FolderName"])
  if not path.exists(folderPath):
    print("The module folder '" + folderPath + "' does not exist", file=sys.stderr)
    exit(-1)

  # Build module
  module = Lecture(moduleName, lecUrls[moduleName], folderPath, config['scriptName'], config['psetFolderName'], config['psetPrefix'])
elif moduleName in config['pcs']:

  # Create and check for module folder
  folderPath = path.join(pcPath, config[moduleName + "FolderName"])
  if not path.exists(folderPath):
    print("The module folder '" + folderPath + "' does not exist", file=sys.stderr)
    exit(-1)
  
  # Build module
  module = PracticalCourse(moduleName, pap.homeUrl, folderPath, config['scriptName'])
else:
  print('The module ' + sys.argv[1] + ' does not exist', file=sys.stderr)
  exit(-1)

# Show home
if len(sys.argv) == 2 or sys.argv[2] == 'home':
  module.showHome()
  exit(0)

# Show other url
if type(module) is Lecture and sys.argv[2] in module.urls:
  if not type(module) is Lecture:
    print('This option is only available for lectures', file=sys.stderr)
    exit(-1)
  module.show(sys.argv[2])
  exit(0)

# Open or download and open problem set
if sys.argv[2] == 'pset':
  # Check for lecture
  if not type(module) is Lecture:
    print('This option is only available for lectures', file=sys.stderr)
    exit(-1)
  # Check for problem set number
  if len(sys.argv) == 3:
    print('You must specify the number of a problem set', file=sys.stderr)
    exit(-1)
  
  # Check if problem set exists locally
  n = int(sys.argv[3])
  psetExists = module.psetCheck(n)
  if not psetExists or '-u' in sys.argv[4:]:
    if not path.exists(module.psetPath()):
      os.mkdir(module.psetPath())
    if not psetExists:
      print('Problem set ' + str(n) + ' was not found locally')
    print('Downloading problem set ' + str(n) + " from '" + pt.serverUrl + "'...")
    print()

    # Create session on the physics tutorial website
    session = requests.Session()
    ptCreateSession(session)

    # Get problem set n by lecture name
    content, success = pt.tryGetPsetByLec(session, module.name, n)
    if not success:
      print('Problem set ' + str(n) + ' seems to be unavailable (yet)', file=sys.stderr)
      exit(-1)
    with open(module.psetPath(n), 'wb') as psetFile:
      psetFile.write(content)
    print('Problem set ' + str(n) + " was saved at '" + module.psetPath(n) + "'")

    # Show problem set n
    module.psetShow(n)
  else:
    # Show problem set n
    module.psetShow(n)
  exit(0)

# Open or download and open script
if sys.argv[2] == 'script':
  scriptExists = module.scriptCheck()
  if not scriptExists or '-u' in sys.argv[3:]:
    if module.name == 'theo4':
      if not scriptExists:
        print('Script was not found locally')
      print("Downloading script from '" + theo4.serverUrl + "'...")
      print()

      # Create session
      session = requests.Session()

      # Download script from homepage
      content = theo4.getScript(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")
    elif module.name == 'gr':
      if not scriptExists:
        print('Script was not found locally')
      print("Downloading script from '" + pt.serverUrl + "'...")
      print()

      # Create session on the physics tutorial website
      session = requests.Session()
      ptCreateSession(session)

      # Download script
      content = pt.getGrScript(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")
    elif module.name == 'pap21':
      if not scriptExists:
        print('Script was not found locally')
      print("Downloading script from '" + pap.serverUrl + "'...")
      print()

      # Create session
      session = requests.Session()

      # Download script from homepage
      content = pap.getPAP21Script(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")
    elif module.name == 'pap22':
      if not scriptExists:
        print('Script was not found locally')
      print("Downloading script from '" + pap.serverUrl + "'...")
      print()

      # Create session
      session = requests.Session()

      # Download script from homepage
      content = pap.getPAP22Script(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")
    else:
      # No Script
      print('There exists no script for this module', file=sys.stderr)
      exit(-1)
    
    # Show script
    module.scriptShow()
  else:
    # Show script
    module.scriptShow()
  exit(0)

print("'" + sys.argv[2] + "' is not a valid option for a lecture", file=sys.stderr)
exit(-1)
