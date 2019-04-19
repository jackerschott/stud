import os
import signal
import sys
from os import path

signal.signal(signal.SIGINT, lambda x,y: { print(), sys.exit(0) })

homePath = path.expanduser('~')
configPath = path.join(homePath, '.config', 'stud')
rcPath = path.join(configPath, 'studrc')
cookiePath = path.join(configPath, 'pt_cjar')

def removeFile(filePath):
  if path.exists(filePath):
    print("rm '" + filePath + "'")
    os.remove(filePath)
def removeDir(dirPath):
  if path.exists(dirPath):
    if os.listdir(dirPath):
      print("Warning: Directory '" + dirPath + "' not empty")
    else:
      print("rm '" + dirPath + "'")
      os.rmdir(dirPath)

removeFile(rcPath)
removeFile(cookiePath)
removeDir(configPath)
