'''
In der test.py Datei, werden die Methoden für die Teilnehmer Ressource getestet
'''
from urllib import response
import requests

BASE = "http://127.0.0.1:5000/"

response=requests.post(BASE + "teilnehmer/1", {"id": 1, "vorname": "Fabian", "name": "Streit",
 "thema": "APIs im Backend", "session_chair":"Quang", "note":0.0}, timeout=5)
input()

response=requests.get(BASE + "teilnehmer/1", timeout=5)
print(response.json())
input()

response=requests.put(BASE + "teilnehmer/1", {"vorname": "Fabian", "name": "Streit",
 "thema": "APIs im Backend mit Flask", "session_chair":"Quang", "note":0.0}, timeout=5)
print(response.json())
input()

response=requests.patch(BASE + "teilnehmer/1", {"thema":"APIs im Backend mit Flask und Django"},
 timeout=5)
print(response.json())
input()

response=requests.delete(BASE + "teilnehmer/1", timeout=5)

input()
