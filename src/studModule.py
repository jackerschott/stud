from browserShow import openUrl, openFile
from os import path

class StudModule:
  def __init__(self, name, homeUrl, folderPath):
    self.name = name
    self.homeUrl = homeUrl
    self.folderPath = folderPath

  def showHome(self):
    openUrl(self.homeUrl)

class Lecture(StudModule):
  def __init__(self, name, urls, folderPath, scriptName, psetDirName, psetPrefix):
    StudModule.__init__(self, name, urls['home'], folderPath)
    self.urls = urls
    self.scriptName = scriptName
    self.psetDirName = psetDirName
    self.psetPrefix = psetPrefix

  def psetPath(self, n=None):
    if n is None:
      return path.join(self.folderPath, self.psetDirName)
    return path.join(self.folderPath, self.psetDirName, self.psetPrefix + str(n) + '.pdf')
  
  def scriptPath(self):
    return path.join(self.folderPath, self.scriptName + '.pdf')

  def show(self, id):
    openUrl(self.urls[id])
  
  def psetCheck(self, n):
    return path.exists(self.psetPath(n))

  def psetShow(self, n):
    openFile(self.psetPath(n))
  
  def scriptCheck(self):
    return path.exists(self.scriptPath())

  def scriptShow(self):
    openFile(self.scriptPath())

class PracticalCourse(StudModule):
  def __init__(self, name, homeUrl, folderPath, scriptName):
    StudModule.__init__(self, name, homeUrl, folderPath)
    self.scriptName = scriptName
  
  def scriptPath(self):
    return path.join(self.folderPath, self.scriptName + '.pdf')

  def scriptCheck(self):
    return path.exists(self.scriptPath())
  
  def scriptShow(self):
    openFile(self.scriptPath())
