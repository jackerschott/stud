# This is the configuration file for the stud tool

# Do not change studPath unless you move the old files to the new directory
dataFolder = '~/.local/share/stud'

config = {
  "lecs": "ex5, qft1",
  "pcs": "fp",
  "lecFolderName": "Lectures",
  "pcFolderName": "PracticalCourses",
  "psetFolderName": "ProblemSets",
  "psetPrefix": "problem_set_",
  "psetTutPrefix": "tutorial_",
  "scriptName": "script"
}

moduleNamesFull = {
  "ex5": "ExperimentalPhysics5",
  "qft1": "QuantumFieldTheory1",
  "fp": "FP"
}

moduleUrls = {
  "ex5": {
    "lsf": "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=307094&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung",
    "home": "https://uebungen.physik.uni-heidelberg.de/vorlesung/20192/1049",
    "psets": "https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=1049",
    "pgroups": "https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=1049",
    "results": "https://uebungen.physik.uni-heidelberg.de/uebungen/ergebnisse.php"
  },
  "qft1": {
    "lsf": "https://lsf.uni-heidelberg.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=306675&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung",
    "home": "https://www.thphys.uni-heidelberg.de/~pawlowski/qftI_19-20.php",
    "psets": "https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=1069",
    "pgroups": "https://uebungen.physik.uni-heidelberg.de/uebungen/liste.php?vorl=1069",
    "results": "https://uebungen.physik.uni-heidelberg.de/uebungen/ergebnisse.php"
  },
  "fp": {
    "home": "https://www.physi.uni-heidelberg.de/Einrichtungen/FP/",
    "status": "https://www.physi.uni-heidelberg.de/cgi-bin/fp-status.pl"
  }
}

