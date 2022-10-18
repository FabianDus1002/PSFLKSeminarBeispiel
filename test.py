from stat import FILE_ATTRIBUTE_READONLY
from urllib import response
import requests

BASE = "http://127.0.0.1:5000/"

response=requests.get(BASE + "teilnehmer/1")
print(response.json())
input()

response=requests.patch(BASE + "teilnehmer/1", {"thema":"APIs im Backend"})
print(response.json())

input()
