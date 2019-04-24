import json
import os
import sys
from os import path
from sys import exit

# Get config file path and output folder from args
configFilePath = ''
outFolder = ''
args = sys.argv[1:]
for i, arg in enumerate(args):
  if path.isfile(arg):
    configFilePath = arg
  if i != 0 and args[i - 1] == '-o' and path.exists(arg):
    outFolder = arg

if not configFilePath:
  print('No valid config file specified', file=sys.stderr)
  exit(-1)
elif not outFolder:
  print('No valid output folder specified', file=sys.stderr)
  exit(-1)

# Load configurations
with open(sys.argv[1]) as configFile:
  configs = json.load(configFile)

# Load module names
with open('config/moduleNames.json') as moduleNamesFile:
  moduleNames = json.load(moduleNamesFile)

# Create module folders
lecs = configs['lecs'].split(', ')
pcs = configs['pcs'].split(', ')
print('Create module folders... ', end='')
for name in moduleNames:
  if name in lecs:
    lecsFolderPath = path.join(outFolder, configs['lecFolderName'])
    lecFolderPath = path.join(lecsFolderPath, configs[name + 'FolderName'])
    if not path.exists(lecsFolderPath):
      os.mkdir(lecsFolderPath)
    if not path.exists(lecFolderPath):
      os.mkdir(lecFolderPath)
  elif name in pcs:
    pcsFolderPath = path.join(outFolder, configs['pcFolderName'])
    pcFolderPath = path.join(pcsFolderPath, configs[name + 'FolderName'])
    if not path.exists(pcsFolderPath):
      os.mkdir(pcsFolderPath)
    if not path.exists(pcFolderPath):
      os.mkdir(pcFolderPath)
print('Done')
