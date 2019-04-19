import os
import subprocess as sp

def openUrl(url):
  NULL = open(os.devnull, 'w')
  sp.Popen(['nohup', 'google-chrome', url, '--new-window'], stdout=NULL, stderr=NULL)

def openFile(path):
  openUrl('file://' + path)
