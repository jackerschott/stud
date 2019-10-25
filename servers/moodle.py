from bs4 import BeautifulSoup
from os import path
from pickle import load, dump

serverUrl = 'https://elearning2.uni-heidelberg.de'
loginUrl = serverUrl + '/login/index.php'
courseBaseUrl = serverUrl + '/course/view.php'

courseIds = {
  'cp' : 20724
}
courseFilePrefixes = {
  'cp' : 'Tutorial '
}
courseNumberFormats = {
  'cp' : '{:n}'
}

def checkForSavedSession(cjarPath):
  return path.exists(cjarPath)

def loadSession(session, cjarPath):
  if checkForSavedSession(cjarPath):
    with open(cjarPath, 'rb') as cjar:
      session.cookies.update(load(cjar))

def saveSession(session, cjarPath):
  with open(cjarPath, 'wb') as cjar:
    dump(session.cookies, cjar)

def checkLoginStatus(session):
  resp = session.get(serverUrl)
  soup = BeautifulSoup(resp.text, 'lxml')
  loginStatusSpan = soup.find('span', { 'class', 'login' })
  return not "Sie sind nicht angemeldet" in loginStatusSpan.contents[0]

def checkPasswordValidity(respText):
  respSoup = BeautifulSoup(respText, 'lxml')
  return respSoup.find('span', { 'class' : 'error' }) is None

def login(session, id, passw):
  resp = session.get(loginUrl)
  loginSoup = BeautifulSoup(resp.text, 'lxml')
  loginToken = loginSoup.find('input', { 'name' : 'logintoken' }).attrs['value']
  resp = session.post(loginUrl, data={ 'username' : id, 'password' : passw, 'logintoken' : loginToken })
  return session, checkPasswordValidity(resp.text)

def tryGetPSet(session, courseId, name):
  resp = session.post(courseBaseUrl, data={ 'id' : courseId })

  courseSoup = BeautifulSoup(resp.text, 'lxml')
  hyperLinkSpans = courseSoup.findAll('span', { 'class' : 'instancename' })
  psetLinks = [s.parent for s in hyperLinkSpans if name in s.contents]
  if len(psetLinks) == 0:
    return None, False

  resp = session.get(psetLinks[0].attrs['href'])
  return resp.content, True

def tryGetPSetByCourse(session, courseName, n):
  namePrefix = courseFilePrefixes[courseName]
  nameNumber = courseNumberFormats[courseName].format(n)
  return tryGetPSet(session, courseIds[courseName], namePrefix + nameNumber)

