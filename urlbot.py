#!/usr/bin/python
import sys
import socket
import string
from urlparse import urlparse
import time
import urllogger
import urldescription
import re

desc = urldescription.URLdescription()

HOST='irc.eagle.y.se'
PORT=6667
NICK='urlbot123'
IDENT='pybot'
REALNAME='s1ash'
CHANNELINIT='#testurltitle'
readbuffer=''
s=socket.socket( )
s.connect((HOST, PORT))
print int(time.time()),s.recv(4096)

print int(time.time()),'NICK '+NICK
s.send('NICK '+NICK+'\n')
print int(time.time()),'USER '+IDENT+' '+HOST+' bla :'+REALNAME
s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\n')

def parsemsg(msg):
    complete=msg[1:].split(':',1)
    info=complete[0].split(' ')
    msgpart=complete[1]
    sender=info[0].split('!')

    msgpart = re.sub(r'[^\x20-\x7e]', '', msgpart)

    for w in msgpart.split(' '):
        o = urlparse(w)
        if len(o.netloc)!=0:
            print int(time.time()),'checking url: "'+w.strip()+'"'
            title = desc.fetchtitle(w.strip())
            if len(title)!=0:
                urllogger.URLlogger(w, title, sender[0]).start()
                print int(time.time()),'PRIVMSG '+info[2]+' :'+title
                s.send('PRIVMSG '+info[2]+' :'+title+'\n')


timer = time.time()
while True:
    line=s.recv(512)
    print int(time.time()),line.rstrip('\n')
    if line.find('Closing Link')!=-1:
        print int(time.time()),'closing link, exiting..'
        sys.exit(1)
    if line.find('Welcome to the Internet Relay Network')!=-1: #FIXME
        print int(time.time()),'JOIN '+CHANNELINIT
        s.send('JOIN '+CHANNELINIT+'\n')
    if line.find('PRIVMSG')!=-1:
        parsemsg(line)
    line=line.rstrip()
    line=line.split()
    if(line[0]=='PING'):
        timer = time.time()
        print int(time.time()),'PONG '+line[1]
        s.send('PONG '+line[1]+'\n')
    if(time.time()-timer>900):
        print int(time.time()),'no PING for 15 min, exiting..'
        sys.exit(1)
