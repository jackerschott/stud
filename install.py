#! /bin/python3
import os
from os import path
import signal
import sys

# Allow keyboard interrupt
signal.signal(signal.SIGINT, lambda x,y: { print(), sys.exit(0)  })

home = path.expanduser('~')
binFolder = path.join(home, '.local/bin')
configFolder = path.join(home, '.config/stud')
dataFolder = path.join(home, '.local/share/stud')
userDataFolder = path.join(home, '.local/share/stud')

configFilePath = path.join(configFolder, 'config.py')

config = {
  'lecs': 'ex5, qft1',
  'pcs': 'fp',
  'lecFolderName': 'Lectures',
  'pcFolderName': 'PracticalCourses',
  'psetFolderName': 'ProblemSets',
  'psetPrefix': 'problem_set_',
  'scriptName': 'script'
}

moduleNamesFull = {
  'ex5': 'ExperimentalPhysics5',
  'qft1': 'QuantumFieldTheory1',
  'fp': 'FP'
}

moduleUrls = {
  'ex5': {
    'lsf': 'https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=307094&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung',
    'home': 'https://uebungen.physik.uni-heidelberg.de/vorlesung/20192/1049',
    'psets': 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=1049',
    'pgroups': 'https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=1049',
    'results': 'https://uebungen.physik.uni-heidelberg.de/uebungen/ergebnisse.php'
  },
  'qft1': {
    'lsf': '',
    'home': '',
    'psets': '',
    'pgroups': '',
    'results': ''
  },
  'fp': {
    'home': ''
  }
}

def cp(src, dest):
  os.system(f'cp {src} {dest}')
  print(dest)

def mkdir(dirPath):
  if not path.isdir(dirPath):
    os.mkdir(dirPath)
  print(dirPath)

# Copy package files
print('Copy files...')
mkdir(f'{dataFolder}')
cp('stud.py', f'{dataFolder}/stud.py')
cp('studModule.py', f'{dataFolder}/studModule.py')
mkdir(f'{dataFolder}/servers')
cp('servers/egm.py', f'{dataFolder}/servers/egm.py')
cp('servers/moodle.py', f'{dataFolder}/servers/moodle.py')
cp('servers/pap.py', f'{dataFolder}/servers/pap.py')
cp('servers/thphys.py', f'{dataFolder}/servers/thphys.py')
print()

# Create binary
print('Generate binary...')
if not path.isfile(f'{binFolder}/stud'):
  os.symlink(f'{dataFolder}/stud.py', f'{binFolder}/stud')
print(f'{binFolder}/stud')
print()

# Create module folders
print('Create module folders...')

while True:
  answerDoChangeUserDataFolder = input(f'The current directory for user data is \'{userDataFolder}\'\nWould you like to change it? [y/n] ')
  if answerDoChangeUserDataFolder in ['', 'y', 'yes']:
    newUserDataFolder = input('Enter new user data directory: ')
    if not path.isdir(newUserDataFolder):
      try:
        os.makedirs(newUserDataFolder)
      except Exception:
        print('error: Could not create the directory.')
        continue
    userDataFolder = newUserDataFolder
    break
  elif answerDoChangeUserDataFolder in ['n', 'no']:
    break

lecs = [lec.strip() for lec in config['lecs'].split(',')]
pcs = [pc.strip() for pc in config['pcs'].split(',')]
if len(lecs) > 0:
  folderPathLecs = path.join(userDataFolder, config['lecFolderName'])
  mkdir(folderPathLecs)
if len(pcs) > 0:
  folderPathPcs = path.join(userDataFolder, config['pcFolderName'])
  mkdir(folderPathPcs)

for moduleName in moduleNamesFull:
  if moduleName in lecs:
    folderPathLec = path.join(folderPathLecs, moduleNamesFull[moduleName])
    mkdir(folderPathLec)
    folderPathPsets = path.join(folderPathLec, config['psetFolderName'])
    mkdir(folderPathPsets)
  elif moduleName in pcs:
    folderPathPc = path.join(userDataFolder, config['pcFolderName'], moduleNamesFull[moduleName])
    mkdir(folderPathPc)
print()

# Generate configuration
print('Generate configuration...')
configPath = os.path.join(configFolder, 'config.py')
if not path.exists(configFolder):
  os.makedirs(configFolder)
if not path.isfile(f'{dataFolder}/config.py'):
  with open('config.py') as configFile:
    configLines = configFile.readlines() 
    for i in range(len(configLines)):
      if 'dataFolder' in configLines[i]:
        configLines[i] = f'dataFolder = \'{userDataFolder}\''
        break
  with open(f'{dataFolder}/config.py', 'w') as configFile:
    configFile.writelines(configLines)
  if not path.isfile(configPath):
    os.symlink(f'{dataFolder}/config.py', configPath)
print(f'{dataFolder}/config.py')
print(configPath)

print('Done... exiting.')

