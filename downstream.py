__author__ = 'x1ang.li'
from urllib2 import urlopen

restreq = urlopen('...')
response = restreq.read()


if sys.platform == 'win32':
    hostaddr = 'C:\Windows\System32\drivers\etc\hosts'
elif sys.platform == 'linux':
    hostaddr = '/etc/hosts'
#open file and read it, then close.
hostfile = open(hostaddr, 'r')
strlist = hostfile.readlines()
hostfile.close()

for a_str in strlist[0:]:
    if a_str.find('gitserver') >= 0 or a_str.find('webserver') >= 0 or a_str.find('dbserver') >= 0 or a_str.find('server') >= 0 or a_str == '\n' or a_str == '\r\n':
        strlist.remove(a_str)
strlist.append("\r\n%s gitserver"%myIp)
strlist.append("\r\n%s webserver"%myIp)
strlist.append("\r\n%s dbserver"%myIp)
strlist.append("\r\n%s server"%myIp)

filestr = ''.join(strlist)

#open file with argument "w",to empty the file
hostfile = open(hostaddr, 'w')
hostfile.write(filestr)
hostfile.close()
print("write < IP to server mapping> to %s !!!"%hostaddr)
