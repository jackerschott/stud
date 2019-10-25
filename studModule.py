import os
from os import path

def openUrl(url):
  os.system(f'nohup xdg-open {url} &> /dev/null')

class StudModule:
  def __init__(self, name, urls, folderPath):
    self.name = name
    self.urls = urls
    self.folderPath = folderPath

  def show(self, id):
    openUrl(self.urls[id])

class Lecture(StudModule):
  def __init__(self, name, urls, folderPath, scriptName, psetDirName, psetPrefix, psetTutPrefix):
    StudModule.__init__(self, name, urls, folderPath)
    self.scriptName = scriptName
    self.psetDirName = psetDirName
    self.psetPrefix = psetPrefix
    self.psetTutPrefix = psetTutPrefix

  def psetPath(self, n=None, isTutorial=False):
    if n is None:
      return path.join(self.folderPath, self.psetDirName)
    if isTutorial:
      return path.join(self.folderPath, self.psetDirName, self.psetTutPrefix + str(n) + '.pdf')
    return path.join(self.folderPath, self.psetDirName, self.psetPrefix + str(n) + '.pdf')
  
  def scriptPath(self):
    return path.join(self.folderPath, self.scriptName + '.pdf')

  def psetCheck(self, n, isTutorial=False):
    return path.exists(self.psetPath(n, isTutorial=False))

  def psetShow(self, n, isTutorial):
    openUrl(self.psetPath(n, isTutorial))
  
  def scriptCheck(self):
    return path.exists(self.scriptPath())

  def scriptShow(self):
    openUrl(self.scriptPath())

class PracticalCourse(StudModule):
  def __init__(self, name, urls, folderPath, scriptName):
    StudModule.__init__(self, name, urls, folderPath)
    self.scriptName = scriptName
  
  def scriptPath(self):
    return path.join(self.folderPath, self.scriptName + '.pdf')

  def scriptCheck(self):
    return path.exists(self.scriptPath())
  
  def scriptShow(self):
    openUrl(self.scriptPath())
