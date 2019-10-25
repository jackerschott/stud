from bs4 import BeautifulSoup

serverUrl = 'https://www.thphys.uni-heidelberg.de'
baseUrls = {
  'theo4': '~/weigand',
  'qft1': '/~pawlowski/qftI_19-20'
}
scriptUrls = {
  'theo4': baseUrls['theo4'] + 'Skript-QM2011/skript.pdf',
  'qft1': baseUrls['qft1'] + '/script/QFT_lectureNotes_19-20.pdf'
}
psetUrls = {
  'qft1': baseUrls['qft1'] + '/qft-uebungen.php'
}

def getScript(session, lecName):
  resp = session.get(serverUrl + scriptUrls[lecName])
  return resp.content

def tryGetPset(session, lecName, name):
  global psetUrls
  if lecName == 'qft1':
    resp = session.get(serverUrl + psetUrls[lecName])
    psetSoup = BeautifulSoup(resp.text, 'lxml')

    hyperLinks = psetSoup.findAll('a')
    boldTextElements = [a.find('b') for a in hyperLinks]
    psetUrls = [b.parent.attrs['href'] for b in boldTextElements if not b is None and b.contents[0].strip() == name]
    if len(psetUrls) == 0:
      return None, False

    resp = session.get(psetUrls[0].replace('\n', ''))
    return resp.content, True
  else:
    raise ValueError()

def tryGetPSetByLec(session, lecName, n, isTutorial=False):
  psetName = f'Tutorial {n}' if isTutorial else f'Exercise {n}'
  return tryGetPset(session, lecName, psetName)

