from bs4 import BeautifulSoup
from os import path
from pickle import load, dump
from fnmatch import filter as fnfilter

serverUrl = 'https://uebungen.physik.uni-heidelberg.de'
egmOverviewUrl = serverUrl + '/uebungen/'
egmLoginUrl = serverUrl + '/uebungen/login.php'
egmListUrl = serverUrl + '/uebungen/liste.php'

grHomeUrl = serverUrl + '/vorlesung/20191/992'

lecids = {
  'ex4' : 999,
  'ex5' : 1049,
  'theo4' : 991,
  'gr' : 992,
  'qft1': 1069
}
lecPsetFileFormats = {
  'ex4' : '{:n}',
  'ex5' : 'Blatt_{:n}_PEP5_WS1920.pdf',
  'theo4' : 'Uebung{:02n}',
  'gr' : 'sheet{:n}',
  'qft1': 'set{:02n}_*.pdf'
}
lecPsetTutFileFormats = {
  'qft1': 'tut{:02n}_*.pdf'
}

def checkForSavedSession(cjarPath):
  return path.exists(cjarPath)

def loadSession(session, cjarPath):
  if checkForSavedSession(cjarPath):
    with open(cjarPath, 'rb') as f:
      session.cookies.update(load(f))

def saveSession(session, cjarPath):
  with open(cjarPath, 'wb') as cjar:
    dump(session.cookies, cjar)

def checkLoginStatus(session):
  resp = session.get(egmOverviewUrl)
  ovSoup = BeautifulSoup(resp.text, 'lxml')
  loginStatusDiv = ovSoup.find('div', { 'class', 'boxRightColumn' })
  return not loginStatusDiv.contents[0].strip() == 'Sie sind nicht eingeloggt'

def checkPasswordValidity(respText):
  respSoup = BeautifulSoup(respText, 'lxml')
  return respSoup.find('div', { 'class' : 'errormsg' }) is None

def login(session, id, passw):
  session.post(egmLoginUrl, data={ 'username' : id, 'submit' : 'senden' })
  resp = session.post(egmLoginUrl, data={ 'loginpass' : passw, 'submit' : 'senden' })
  return session, checkPasswordValidity(resp.text)

def tryGetPSet(session, lecid, fileName):
  resp = session.post(egmListUrl, data={ 'vorl' : str(lecid) })

  lecSoup = BeautifulSoup(resp.text, 'lxml')
  listItemFiles = lecSoup.find('div', { 'class' : 'materialien' })
  hyperlinks = listItemFiles.findAll('a')

  psetLinks = [link for link in hyperlinks if len(fnfilter(link.contents, fileName)) > 0]
  if len(psetLinks) == 0:
    return None, False
  
  resp = session.get(serverUrl + psetLinks[0].attrs['href'])
  return resp.content, True

def tryGetPSetByLec(session, lecName, n, isTutorial=False):
  if isTutorial:
    fileName = lecPsetTutFileFormats[lecName].format(n)
  else:
    fileName = lecPsetFileFormats[lecName].format(n)
  return tryGetPSet(session, lecids[lecName], fileName)

def getGrScript(session):
  resp = session.get(grHomeUrl)
  homeSoup = BeautifulSoup(resp.text, 'lxml')
  divRightArea1 = homeSoup.find('div', { 'id' : 'rightarea-5868' })
  scriptHyperlink = divRightArea1.find('a')
  resp = session.get(serverUrl + scriptHyperlink.attrs['href'])
  return resp.content
