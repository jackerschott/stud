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
  def __init__(self, name, urls, folderPath):
    StudModule.__init__(self, name, urls['home'], folderPath)
    self.urls = urls
  
  def psetPath(self, n):
    return path.join(self.folderPath, 'psets', 'pset' + str(n) + '.pdf')
  
  def scriptPath(self):
    return path.join(self.folderPath, 'script.pdf')

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

  @staticmethod
  def urlsFromFile(path):
    urls = {}
    with open(path) as urlFile:
      for line in urlFile:
        if line.strip() == '':
          continue
        id, url = line.split(' - ')
        urls[id] = url
    return urls

class PracticalCourse(StudModule):
  def __init__(self, name, homeUrl, folderPath):
    StudModule.__init__(self, name, homeUrl, folderPath)
