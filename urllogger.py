#! /usr/bin/env python
import threading
import sqlite3 as lite
import sys
import datetime
import htmlprinter

class URLlogger(threading.Thread):
    def __init__(self, url, text, nick):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.url = url
        self.text = text
        self.nick = nick
        self.con = None
        self.dbname = 'url.db'
        self.htmlname = 'urls.html'

    def __del__(self):
        if self.con:
            self.con.close()

    def connect(self):
        try:
            self.con = lite.connect(self.dbname)
            self.cur = self.con.cursor()
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def insert(self):
        data = (str(datetime.datetime.now()), self.url, self.text, self.nick)
        try:
            self.cur.execute("INSERT INTO url VALUES(?, ?, ?, ?)", data)
            self.con.commit()
        except lite.Error, e:
            if self.con:
                self.con.rollback()
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def run(self):
        self.connect()
        self.insert()
        htmlprinter.PrintHTML(self.htmlname, self.dbname)
