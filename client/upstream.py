__author__ = 'x1ang.li'

from client.common import *

def checkip():
    r = reqget('/ip/')
    if (r.status_code != 200):
        raise Exception('HTTP request error. HTTP status code %i' % r.status_code)
    rjson = r.json()
    ip = rjson['ip']
    return ip

def haschanged(newip):
    r = reqgetauth('/silos/'+clicfg['silo_id'])
    rjson = r.json()
    dnsrecordsjson = rjson['dnsrecords']
    for record in dnsrecordsjson:
        if record['hostname'] in clicfg['hostnames']:
            if newip != record['ip']:
                return True
    return False

def puship(newip):
    silo_id = clicfg['silo_id']
    dnsrecords = [ {'hostname':hostname, 'ip': newip} for hostname in clicfg['hostnames'] ] # Python list comprehension
    payload = {'id': silo_id, 'dnsrecords': dnsrecords}
    r = requests.put('/silos/' + silo_id, data = payload, auth = (clicfg['username'], clicfg['password']))
    if r.status_code != requests.codes.ok:
        raise Exception('Unable to call the server')


if __name__ == '__main__':
    ip = checkip()
    print ('Current IP is {}'.format(ip))
    if (haschanged(ip)):
        print('IP has changed. Pushing to server')
        puship(ip)
        print('Upstream push is finished. ')

