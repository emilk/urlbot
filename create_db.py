#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys

con = lite.connect('url.db')

with con:
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data
    cur.execute("CREATE TABLE IF NOT EXISTS url(time datetime default current_timestamp, url text primary key, title text, nick text)")
