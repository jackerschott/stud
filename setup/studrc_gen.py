import json
import sys
from os import path
from sys import exit

# Set out path
outFilePath = 'studrc.json'
if '-o' in sys.argv:
  i = sys.argv.index('-o')
  if len(sys.argv) <= i + 1:
    print()
    exit(-1)
  outFilePath = sys.argv[i + 1]

# Load default configuration
with open('config/studrcDefault.json') as configFile:
  config = json.load(configFile)

with open('config/moduleNames.json') as moduleNameFile:
  moduleNames = json.load(moduleNameFile)

# Get default studPath and modules
studPath = path.expanduser(config['studPath'])
lecs = config['lecs'].split(', ')
pcs = config['pcs'].split(', ')

# Set stud path
studPath_ = input('Set main studies folder path [ ' + studPath + ' ]: ')
print()

config['studPath'] = studPath_ if studPath_ != '' else studPath

# Set modules
lecs_ = lecs.copy()
for lec in lecs_:
  resp = None
  while resp != '' and resp != 'y' and resp != 'n':
    resp = input("Add lecture '" + lec + "' (" + moduleNames[lec] + ") to configuration? [y/n] ")
  if resp == 'n':
    lecs.remove(lec)
  else:
    config[lec + "FolderName"] = moduleNames[lec]
print()

pcs_ = pcs.copy()
for pc in pcs_:
  resp = None
  while resp != '' and resp != 'y' and resp != 'n':
    resp = input("Add practical course '" + pc + "' (" + moduleNames[pc] + ") to configuration? [y/n] ")
  if resp == 'n':
    pcs.remove(pc)
  else:
    config[pc + "FolderName"] = moduleNames[pc]
print()

config['lecs'] = ', '.join(lecs)
config['pcs'] = ', '.join(pcs)

# Generating configuration
print('Generating configuration...')
with open(outFilePath, 'w') as outFile:
  json.dump(config, outFile, indent=2)
