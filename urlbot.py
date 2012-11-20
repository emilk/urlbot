#!/usr/bin/python
import sys
import socket
import string
from urlparse import urlparse
import urllib2
import re

HOST='irc.eagle.y.se'
PORT=6667
NICK='urlbot123'
IDENT='pybot'
REALNAME='s1ash'
CHANNELINIT='#testurltitle'
readbuffer=''
s=socket.socket( )
s.connect((HOST, PORT))
print s.recv(4096)
s.send('NICK '+NICK+'\n')
s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\n')

def fetchtitle(url):
    inTitle=False
    title=''
    try:
        page = urllib2.urlopen(url)
    except urllib2.URLError:
        return "I'm sorry dave..."

    for html in page.readlines():
        match = re.search('\<title.*?\>(.*?)\<\/title\>', html)
        if match:
            title=match.group(1)
            break
        match = re.search('\<title.*?\>', html)
        if match:
            inTitle=True
        match = re.search('\<title.*?\>(.*?)', html)
        if match:
            title=title+match.group(1)
            continue
        match = re.search('(.*?)\<\/title\>', html)
        if match:
            title=title+match.group(1)
            break
        if inTitle:
            title=title+' '+html
    title=title.strip()
    return title

def parsemsg(msg):
    complete=msg[1:].split(':',1)
    info=complete[0].split(' ')
    msgpart=complete[1]
    sender=info[0].split('!')

    for w in msgpart.split(' '):
        o = urlparse(w)
        if len(o.netloc)!=0:
            title = fetchtitle(w)
            if len(title)!=0:
                s.send('PRIVMSG '+info[2]+' :'+title+'\n')

while True:
    line=s.recv(512)
    print line
    if line.find('Closing Link')!=-1:
        sys.exit(1)
    if line.find('Welcome to the Internet Relay Network')!=-1: #FIXME
        s.send('JOIN '+CHANNELINIT+'\n')
    if line.find('PRIVMSG')!=-1:
        parsemsg(line)
    line=line.rstrip()
    line=line.split()
    if(line[0]=='PING'):
        s.send('PONG '+line[1]+'\n')
