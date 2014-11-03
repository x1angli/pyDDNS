__author__ = 'x1ang.li'

import requests

clicfg = {
    'endpoint' : 'http://localhost:81',
    'username' : 'cumuli',
    'password' : 'cumuli123',
    'silo_id'  : 'silo1',
    'hostnames': [
        'webserver', 'dbserver'
    ]
}



def reqplain(path):
    return requests.get(clicfg['endpoint'] + path)

def reqauthed(path):
    return requests.get(clicfg['endpoint'] + path, auth=(clicfg['username'], clicfg['password']))
