import os
import signal
import sys
from os import path

signal.signal(signal.SIGINT, lambda x,y: { print(), sys.exit(0) })

homePath = path.expanduser('~')
configPath = path.join(homePath, '.config', 'stud')
rcPath = path.join(configPath, 'studrc')

# Translate abbreviations
moduleNames = {
  'ex4' : 'Experimental physics 4',
  'theo4' : 'Theoretical physics 4',
  'gr' : 'General relativity',
  'pap1' : 'Practical physics course 1',
  'pap21' : 'Practical physics course 2.1',
  'pap22' : 'Practical physics course 2.2'
}

# Standard configuration
lecPath = path.join(homePath, 'Documents/Studies/Lectures')
pcPath = path.join(homePath, 'Documents/Studies/Practical Courses')
lecs = ['ex4', 'theo4', 'gr']
pcs = ['pap1', 'pap21', 'pap22']
scriptName = 'script'
lecPsetDirName = 'psets'
lecPsetPrefix = 'pset'

def createFolder(dirPath):
  print("Creating '" + dirPath + "'...")
  if not path.exists(dirPath):
    try:
      os.mkdir(dirPath)
    except:
      print("Error: The path '" + dirPath + "' is invalid", file=sys.stderr)
      abort()

def abort():
  print('Abort', file=sys.stderr)
  exit(-1)

if not path.exists(configPath):
  # Choose paths for lectures and practical courses
  newLecPath = input("Choose lecture folder [ '" + lecPath + "' ]: ")
  if newLecPath == '':
    newLecPath = lecPath
  newPcPath = input("Choose practical course folder [ '" + pcPath + "' ]: ")
  if newPcPath == '':
    newPcPath = pcPath
  print()

  # Choose which lectures and practical courses to configure
  newLecs = []
  for lec in lecs:
    answer = input("Add lecture '" + lec + "' (" + moduleNames[lec] + ") to configuration? [y/n] ")
    if answer == 'y' or answer == '':
      newLecs.append(lec)
    elif answer != 'n':
      abort()
  newPcs = []
  for pc in pcs:
    answer = input("Add practical course '" + pc + "' (" + moduleNames[pc] + ") to configuration? [y/n] ")
    if answer == 'y' or answer == '':
      newPcs.append(pc)
    elif answer != 'n':
      print('Abort', file=sys.stderr)
      exit(-1)
  if len(newLecs) == 0 and len(newPcs) == 0:
    print('No module was selected', file=sys.stderr)
    abort()
  print()

  # Choose script and problem set directory name, as well as problem set prefix
  newScriptName = input('Choose module script name [ ' + scriptName + ' ]: ')
  if newScriptName == '':
    newScriptName = scriptName
  newLecPsetDirName = input('Choose directory name for problem sets [ ' + lecPsetDirName + ' ]: ')
  if newLecPsetDirName == '':
    newLecPsetDirName = lecPsetDirName
  newLecPsetPrefix = input('Choose prefix for problem sets [ ' + lecPsetPrefix + ' ]: ')
  if newLecPsetPrefix == '':
    newLecPsetPrefix = lecPsetPrefix
  print()

  # Creating lecture and practical course directories
  createFolder(newLecPath)
  for lec in newLecs:
    createFolder(path.join(newLecPath, lec))
  createFolder(newPcPath)
  for pc in newPcs:
    createFolder(path.join(newPcPath, pc))

  # Creating resource file
  print("Creating '" + rcPath + "'...")
  os.mkdir(configPath)
  with open(rcPath, 'w') as rcFile:
    print('lecPath', ':', newLecPath, file=rcFile)
    print('pcPath', ':', newPcPath, file=rcFile)
    print('', file=rcFile)
    print('lecs', ':', ', '.join(newLecs), file=rcFile)
    print('pcs', ':', ', '.join(newPcs), file=rcFile)
    print('', file=rcFile)
    print('scriptName', ':', newScriptName, file=rcFile)
    print('lecPsetDirName', ':', newLecPsetDirName, file=rcFile)
    print('lecPsetPrefix', ':', newLecPsetPrefix, file=rcFile)
    print('', file=rcFile)

else:
  print("Error: The path '" + configPath + "' does already exist", file=sys.stderr)
  abort()
