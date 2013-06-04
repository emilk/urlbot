#!/usr/bin/python
import sys
import socket
import string
from urlparse import urlparse
import time
import urllogger
import urldescription
import re

class URLBot():
    def __init__(self, host, port, nick, ident, name, chan):
        self.host = host
        self.port = port
        self.nick = nick
        self.ident = ident
        self.name = name
        self.chan = chan
        self.desc = urldescription.URLdescription()
        self.welcome = 'Welcome to the Internet Relay Network' #FIXME
        self.sock = socket.socket( )

    def parsemsg(self):
        complete=self.line[1:].split(':',1)
        info=complete[0].split(' ')
        msgpart=complete[1]
        sender=info[0].split('!')

        msgpart = re.sub(r'[^\x20-\x7e]', '', msgpart)

        for w in msgpart.split(' '):
            o = urlparse(w)
            if len(o.netloc)!=0:
                print int(time.time()),'checking url: "'+w.strip()+'"'
                title = self.desc.fetchtitle(w.strip())
                if len(title)!=0:
                    urllogger.URLlogger(w, title, sender[0]).start()
                    print int(time.time()),'PRIVMSG '+info[2]+' :'+title
                    if w.strip() != title:
                        self.sock.send('PRIVMSG '+info[2]+' :'+title+'\n')

    def run(self):
        readbuffer=''
        self.sock.connect((self.host, self.port))
        print int(time.time()),self.sock.recv(4096)

        print int(time.time()),'NICK '+self.nick
        self.sock.send('NICK '+self.nick+'\n')
        print int(time.time()),'USER '+self.ident+' '+self.host+' bla :'+self.name
        self.sock.send('USER '+self.ident+' '+self.host+' bla :'+self.name+'\n')

        timer = time.time()
        while True:
            self.line=self.sock.recv(512)
            print int(time.time()),self.line.rstrip('\n')
            if self.line.find('Closing Link')!=-1:
                print int(time.time()),'closing link, exiting..'
                sys.exit(1)
            if self.line.find(self.welcome)!=-1:
                print int(time.time()),'JOIN '+self.chan
                self.sock.send('JOIN '+self.chan+'\n')
            if self.line.find('PRIVMSG')!=-1:
                self.parsemsg()
            self.line=self.line.rstrip()
            self.line=self.line.split()
            if(self.line[0]=='PING'):
                timer = time.time()
                print int(time.time()),'PONG '+self.line[1]
                self.sock.send('PONG '+self.line[1]+'\n')
            if(time.time()-timer>900):
                print int(time.time()),'no PING for 15 min, exiting..'
                sys.exit(1)
