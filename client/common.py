
import requests

from client.config import clicfg

def reqget(path):
    return requests.get(clicfg['endpoint'] + path)

def reqgetauth(path):
    return requests.get(clicfg['endpoint'] + path, auth=(clicfg['username'], clicfg['password']))

