#! /bin/python3
import os
from os import path
import signal
import sys

# Allow keyboard interrupt
signal.signal(signal.SIGINT, lambda x,y: { print('Done... exiting.'), sys.exit(0) })

home = path.expanduser('~')
binFolder = path.join(home, '.local/bin')
configFolder = path.join(home, '.config/stud')
cacheFolder = path.join(home, '.cache/stud')
dataFolder = path.join(home, '.local/share/stud')

configFilePath = path.join(configFolder, 'config.py')

def rm(filePath):
  if not path.exists(filePath):
    return
  os.system(f'rm {filePath}')
  print(f'{filePath}')

def rmr(dirPath):
  if not os.exists(dirPath):
    return
  names = os.listdir(dirPath)
  if not names:
    rmdir(dirPath)
    return 
  for name in names:
    path = path.join(dirPath, name)
    if os.isdir(path):
      rmr(path)
    else:
      rm(path)

def rmdir(dirPath):
  if path.exists(dirPath) and path.isdir(dirPath):
    if not os.listdir(f'{dirPath}'):
      os.system(f'rmdir {dirPath}')
      print(f'{dirPath}')
    else:
      print(f'\'{dirPath}\' not empty, so not removed')

# Remove package files
print('Remove package files...')
rm(f'{configFilePath}')
rmdir(f'{configFolder}')
rm(f'{dataFolder}/servers/thphys.py')
rm(f'{dataFolder}/servers/pap.py')
rm(f'{dataFolder}/servers/moodle.py')
rm(f'{dataFolder}/servers/egm.py')
if path.isdir(f'{dataFolder}/servers/__pycache__'):
  os.system(f'rm -r {dataFolder}/servers/__pycache__')
  print(f'{dataFolder}/servers/__pycache__')
rmdir(f'{dataFolder}/servers')
rm(f'{dataFolder}/config.py')
rm(f'{dataFolder}/studModule.py')
rm(f'{dataFolder}/stud.py')
if path.isdir(f'{dataFolder}/__pycache__'):
  os.system(f'rm -r {dataFolder}/__pycache__')
  print(f'{dataFolder}/__pycache__')
rmdir(f'{dataFolder}')
if path.isdir(f'{cacheFolder}'):
  os.system(f'rm -r {cacheFolder}')
  print(f'{cacheFolder}')
print()

# Done
print('Done... exiting.')

