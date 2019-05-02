from bs4 import BeautifulSoup
from os import path
from pickle import load, dump

serverUrl = 'https://uebungen.physik.uni-heidelberg.de'
ptOverviewUrl = serverUrl + '/uebungen/'
ptLoginUrl = serverUrl + '/uebungen/login.php'
ptListUrl = serverUrl + '/uebungen/liste.php'

grHomeUrl = serverUrl + '/vorlesung/20191/992'

lecids = {
  'ex4' : 999,
  'theo4' : 991,
  'gr' : 992
}
lecFilePrefixes = {
  'ex4' : '',
  'theo4' : 'Uebung',
  'gr' : 'sheet'
}
lecNumberFormats = {
  'ex4' : '{:n}',
  'theo4' : '{:02n}',
  'gr' : '{:n}'
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
  resp = session.get(ptOverviewUrl)
  ovSoup = BeautifulSoup(resp.text, 'lxml')
  loginStatusDiv = ovSoup.find('div', { 'class', 'boxRightColumn' })
  return not loginStatusDiv.contents[0].strip() == 'Sie sind nicht eingeloggt'

def checkPasswordValidity(respText):
  respSoup = BeautifulSoup(respText, 'lxml')
  return respSoup.find('div', { 'class' : 'errormsg' }) is None

def login(session, id, passw):
  session.post(ptLoginUrl, data={ 'username' : id, 'submit' : 'senden' })
  resp = session.post(ptLoginUrl, data={ 'loginpass' : passw, 'submit' : 'senden' })
  return session, checkPasswordValidity(resp.text)

def tryGetPSet(session, lecid, fileName):
  resp = session.post(ptListUrl, data={ 'vorl' : str(lecid) })

  lecSoup = BeautifulSoup(resp.text, 'lxml')
  listItemFiles = lecSoup.find('div', { 'class' : 'materialien' })
  hyperlinks = listItemFiles.findAll('a')
  psetLinks = [link for link in hyperlinks if fileName in link.contents]
  if len(psetLinks) == 0:
    return None, False
  
  resp = session.get(serverUrl + psetLinks[0].attrs['href'])
  return resp.content, True

def tryGetPSetByLec(session, lecName, n):
  filePrefix = lecFilePrefixes[lecName]
  fileNumber = lecNumberFormats[lecName].format(n)
  return tryGetPSet(session, lecids[lecName], filePrefix + fileNumber + '.pdf')

def getGrScript(session):
  resp = session.get(grHomeUrl)
  homeSoup = BeautifulSoup(resp.text, 'lxml')
  divRightArea1 = homeSoup.find('div', { 'id' : 'rightarea-5868' })
  scriptHyperlink = divRightArea1.find('a')
  resp = session.get(serverUrl + scriptHyperlink.attrs['href'])
  return resp.content
