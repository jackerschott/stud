
serverUrl = 'https://www.physi.uni-heidelberg.de'
homeUrl = serverUrl + '/cgi-bin/ap-status.pl'
scriptUrl = serverUrl + '/Einrichtungen/AP/info/PAP2_2019/'
scriptPAP21Url = scriptUrl + 'PAP21_MThOges0419.pdf'
scriptPAP22Url = scriptUrl + 'PAP22_Elektr_Radioak_0419.pdf'

def getPAP21Script(session):
  resp = session.get(scriptPAP21Url)
  return resp.content

def getPAP22Script(session):
  resp = session.get(scriptPAP22Url)
  return resp.content
