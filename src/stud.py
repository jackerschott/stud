#!/usr/bin/python3
import os
import requests
import servers.theo4 as theo4
import servers.pap as pap
import servers.pt as pt
import signal
import sys
from getpass import getpass
from studModule import StudModule, Lecture, PracticalCourse
from os import path

signal.signal(signal.SIGINT, lambda x,y: { print(), sys.exit(0) })

homePath = path.expanduser('~')

def loadConfigs(path):
  configs = {}
  with open(path) as configFile:
    for line in configFile:
      line = line.strip()
      if line == '':
        continue
      key, config = line.split(' : ')
      config = config.split(', ')
      if len(config) == 1:
        config = config[0]
      configs[key] = config
  return configs

# Load configurations
# configPath = path.join(homePath, '.config', 'stud')
configPath = path.join(homePath, '.config', 'stud')
configFile = path.join(configPath, 'studrc')
ptCookiePath = path.join(configPath, 'pt_cjar')
configs = loadConfigs(configFile)
lecPath = configs['lecPath']
pcPath = configs['pcPath']

lecUrls = {
  'ex4' : {
    'lsf' : 'https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=295596&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung',
    'psets' : 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=999',
    'pgroups' : 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=999',
    'home' : 'https://uebungen.physik.uni-heidelberg.de/vorlesung/20191/pep4'
  },
  'theo4' : {
    'lsf' : 'https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=295616&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung',
    'psets' : 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=991',
    'pgroups' : 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=991',
    'home' : 'https://www.thphys.uni-heidelberg.de/~hebecker/QM/qm.html'
  },
  'gr' : {
    'lsf' : 'https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=295624&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung',
    'psets' : 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=992',
    'pgroups' : 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=992',
    'home' : 'https://uebungen.physik.uni-heidelberg.de/vorlesung/20191/992'
  }
}

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
if moduleName in configs['lecs']:
  
  # Create and check for module folder
  folderPath = path.join(lecPath, moduleName)
  if not path.exists(folderPath):
    print("The module folder '" + folderPath + "' does not exist", file=sys.stderr)
    exit(-1)

  # Build module
  module = Lecture(moduleName, lecUrls[moduleName], folderPath, configs['scriptName'], configs['lecPsetDirName'], configs['lecPsetPrefix'])
elif moduleName in configs['pcs']:

  # Create and check for module folder
  folderPath = path.join(pcPath, moduleName)
  if not path.exists(folderPath):
    print("The module folder '" + folderPath + "' does not exist", file=sys.stderr)
    exit(-1)
  
  # Build module
  module = PracticalCourse(moduleName, pap.homeUrl, folderPath, configs['scriptName'])
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
  if not module.psetCheck(n):
    if not path.exists(module.psetPath()):
      os.mkdir(module.psetPath())
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
    if module.name == 'theo4':
      print('Script was not found locally')
      print("Searching for script on '" + theo4.serverUrl + "'...")
      print()

      # Create session
      session = requests.Session()

      # Download script from homepage
      content = theo4.getScript(session)
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
