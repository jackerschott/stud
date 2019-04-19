
serverUrl = 'https://www.thphys.uni-heidelberg.de'
scriptUrl = serverUrl + '/~weigand/Skript-QM2011/skript.pdf'

def getScript(session):
  resp = session.get(scriptUrl)
  return resp.content
