__author__ = 'x1ang.li'

import sys, os

from client.common import *

def updateHostFile():
    r = reqplain('/silos/'+clicfg['silo_id'])
    if (r.status_code != 200):
        raise Exception('HTTP request error. HTTP status code ' + r.status_code)
    rjson = r.json()
    if not rjson:
        raise Exception('Unable to get the response json')
    if not 'dnsrecords' in rjson:
        raise Exception('Malformed response. It should contain a "dnsrecord" key')
    dnsrecordsjson = rjson['dnsrecords']

    if sys.platform == 'win32':
        hostaddr = '{SystemRoot}\\system32\\drivers\\etc\\hosts' % (os.environ.get('SystemRoot'))
    elif sys.platform == 'linux':
        hostaddr = '/etc/hosts'
    else:
        raise Exception('The host file\'s address is unknown.')

    #open file and read it, then close.
    hostfile = open(hostaddr, 'r')
    curlines = hostfile.readlines() # current lines
    hostfile.close()

    newlines = list(filter(shouldkeep, curlines))
    for dnsrecord in dnsrecordsjson:
        newlines.append('{ip}\t{hostname}'.format(**dnsrecord))
    newfilestr = os.linesep.join(newlines)

    hostfile = open(hostaddr, 'w')     #open file with argument "w",to empty the file
    hostfile.write(newfilestr)
    hostfile.close()

def shouldkeep(line):
    tokens = line.split()
    if (len(tokens) < 2):
        return True
    hostname = tokens[0]
    if (hostname in clicfg['hostnames']):
        return False
    return True

if __name__ == '__main__':
    updateHostFile()
    print('Done updating the host file')



