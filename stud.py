#! /bin/python3
from getpass import getpass
import json
import os
from os import path
import requests
import servers.moodle as moodle
import servers.thphys as thphys
import servers.pap as pap
import servers.egm as egm
import signal
from studModule import StudModule, Lecture, PracticalCourse
import sys
from sys import exit
from config import dataFolder, config, moduleNamesFull, moduleUrls 

# Allow keyboard interrupt
signal.signal(signal.SIGINT, lambda x,y: { print(), sys.exit(0) })

# Load configurations
homePath = path.expanduser('~')
cacheDirPath = path.join(homePath, '.cache', 'stud')
moodleCookiePath = path.join(cacheDirPath, 'moodle_cjar')
egmCookiePath = path.join(cacheDirPath, 'egm_cjar')

lecPath = path.join(dataFolder, config['lecFolderName'])
pcPath = path.join(dataFolder, config['pcFolderName'])

def moodleCreateSession(session):
  # Check for cache dir
  if not path.isdir(cacheDirPath):
    os.makedirs(cacheDirPath)
  # Login or use old session
  moodle.loadSession(session, moodleCookiePath)
  if not moodle.checkForSavedSession(egmCookiePath) or not moodle.checkLoginStatus(session):
    # Get username and password
    id = input("username for '" + moodle.serverUrl + "': ")
    passw = getpass("password for '" + moodle.serverUrl + "': ")
    print()

    # Login
    session, success = moodle.login(session, id, passw)
    if not success:
      print('Invalid username or password', file=sys.stderr)
      exit(-1)
    moodle.saveSession(session, egmCookiePath)

def egmCreateSession(session):
  # Check for cache dir
  if not path.isdir(cacheDirPath):
    os.makedirs(cacheDirPath)
  # Login or use old session
  egm.loadSession(session, egmCookiePath)
  if not egm.checkForSavedSession(egmCookiePath) or not egm.checkLoginStatus(session):
    # Get username and password
    id = input("username for '" + egm.serverUrl + "': ")
    passw = getpass("password for '" + egm.serverUrl + "': ")
    print()

    # Login
    session, success = egm.login(session, id, passw)
    if not success:
      print('Invalid username or password', file=sys.stderr)
      exit(-1)
    egm.saveSession(session, egmCookiePath)

# Check for module
if len(sys.argv) <= 1:
  print('You must specify a module', file=sys.stderr)
  exit(-1)

# Build module
moduleName = sys.argv[1]
if moduleName in config['lecs']:
  
  # Create and check for module folder
  folderPath = path.join(lecPath, moduleNamesFull[moduleName])
  if not path.exists(folderPath):
    print("The module folder '" + folderPath + "' does not exist", file=sys.stderr)
    exit(-1)

  # Build module
  module = Lecture(moduleName, moduleUrls[moduleName], folderPath, config['scriptName'], config['psetFolderName'], config['psetPrefix'], config['psetTutPrefix'])
elif moduleName in config['pcs']:

  # Create and check for module folder
  folderPath = path.join(pcPath, moduleNamesFull[moduleName])
  if not path.exists(folderPath):
    print("The module folder '" + folderPath + "' does not exist", file=sys.stderr)
    exit(-1)
  
  # Build module
  module = PracticalCourse(moduleName, pap.homeUrl, folderPath, config['scriptName'])
else:
  print('The module ' + sys.argv[1] + ' does not exist', file=sys.stderr)
  exit(-1)

# Show home
if len(sys.argv) == 2:
  module.show('home')
  exit(0)

# Show url
if sys.argv[2] in module.urls:
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
  isTutorial = '-t' in sys.argv[4:]
  psetExists = module.psetCheck(n, isTutorial)
  if not psetExists or '-u' in sys.argv[4:]:
    if not path.exists(module.psetPath()):
      os.mkdir(module.psetPath())
    if not psetExists:
      print('Problem set ' + str(n) + ' was not found locally')

    if module.name == 'cp':
      print('Downloading problem set ' + str(n) + " from '" + moodle.serverUrl + "'...")
      print()

      # Create session on moodle
      session = requests.Session()
      moodleCreateSession(session)

      # Get problem set n by lecture name
      content, success = moodle.tryGetPSetByCourse(session, module.name, n)
    if module.name == 'qft1':
      print('Downloading problem set ' + str(n) + " from '" + egm.serverUrl + "'...")
      print()

      # Create session on the physics isTutorial website
      session = requests.Session()
      egmCreateSession(session)
      
      # Get problem set n by lecture name
      content, success = egm.tryGetPSetByLec(session, module.name, n, isTutorial)
    else:
      # Create session on the physics tutorial website
      session = requests.Session()
      egmCreateSession(session)

      # Get problem set n by lecture name
      content, success = egm.tryGetPSetByLec(session, module.name, n)
    
    if not success:
      print('Problem set ' + str(n) + ' seems to be unavailable (yet)', file=sys.stderr)
      exit(-1)
    with open(module.psetPath(n, isTutorial), 'wb') as psetFile:
      psetFile.write(content)
    print('Problem set ' + str(n) + " was saved at '" + module.psetPath(n, isTutorial) + "'")

    # Show problem set n
    module.psetShow(n, isTutorial)
  else:
    # Show problem set n
    module.psetShow(n, isTutorial)
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
      print("Downloading script from '" + egm.serverUrl + "'...")
      print()

      # Create session on the physics tutorial website
      session = requests.Session()
      egmCreateSession(session)

      # Download script
      content = egm.getGrScript(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")
    elif module.name == 'qft1':
      if not scriptExists:
        print('Script was not found locally')
      print("Downloading script from '" + thphys.serverUrl + "'...")
      print()

      # Create session
      session = requests.Session()
      
      # Download script
      content = thphys.getScript(session, module.name)
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
