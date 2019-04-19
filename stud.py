#!/usr/bin/python3
import htheo4
import pt
import requests
import sys
from getpass import getpass
from studModule import StudModule, Lecture, PracticalCourse
from os import path

lecPath = '/home/jona/Documents/Studies/Lectures'
papPath = '/home/jona/Documents/Studies/PAP2'

papHomeUrl = 'https://www.physi.uni-heidelberg.de/cgi-bin/ap-status.pl'

def ptCreateSession(session):
  # Login or use old session
  pt.loadSession(session)
  if not pt.checkForSavedSession() or not pt.checkLoginStatusPT(session):
    # Get username and password
    id = input("username for '" + pt.serverUrl + "': ")
    passw = getpass("password for '" + pt.serverUrl + "': ")
    print()

    # Login
    session, success = pt.loginPT(session, id, passw)
    if not success:
      print('Invalid username or password', file=sys.stderr)
      exit(-1)
    pt.saveSession(session)

# Check for module
if len(sys.argv) <= 1:
  print('You must specify a module', file=sys.stderr)
  exit(-1)

# Build module
moduleName = sys.argv[1]
if path.exists(path.join(lecPath, moduleName)):
  folderPath = path.join(lecPath, moduleName)
  urls = Lecture.urlsFromFile(path.join(lecPath, moduleName, 'urls.txt'))
  module = Lecture(moduleName, urls, folderPath)
elif moduleName == 'pap':
  module = PracticalCourse('pap', papHomeUrl, papPath)
else:
  print('The module ' + sys.argv[1] + ' does not exist', file=sys.stderr)
  exit(-1)

# Show home
if len(sys.argv) == 2 or sys.argv[2] == 'home':
  module.showHome()
  exit(0)

# Show other url
if sys.argv[2] in module.urls:
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
  if not module.psetCheck(n):
    print('Problem set ' + str(n) + ' was not found locally')
    print('Searching for problem set ' + str(n) + " on '" + pt.serverUrl + "'...")
    print()

    # Create session on the physics tutorial website
    session = requests.Session()
    ptCreateSession(session)

    # Get problem set n by lecture name
    content, success = pt.tryGetPsetByLec(session, module.name, n)
    if not success:
      print('Problem set ' + str(n) + ' seems to be unavailable yet', file=sys.stderr)
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
  if not module.scriptCheck():
    if module.name == 'ex4':
      # No Script
      print('There exists no script for this lecture', file=sys.stderr)
      exit(-1)
    elif module.name == 'theo4':
      print('Script was not found locally')
      print("Searching for script on '" + htheo4.serverUrl + "'...")
      print()

      # Create session
      session = requests.Session()

      # Download script from homepage
      content = htheo4.getScript(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")
    elif module.name == 'gr':
      print('Script was not found locally')
      print("Searching for script on '" + pt.serverUrl + "'...")
      print()

      # Create session on the physics tutorial website
      session = requests.Session()
      ptCreateSession(session)

      # Download script
      content = pt.getGrScript(session)
      with open(module.scriptPath(), 'wb') as scriptFile:
        scriptFile.write(content)
      print("Script was saved at '" + module.scriptPath() + "'")

    # Show script
    module.scriptShow()
  else:
    # Show script
    module.scriptShow()
