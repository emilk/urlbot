#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
import time
import datetime

class PrintHTML():
    def __init__(self, filename, database):
        con = lite.connect(database)
        self.cur = con.cursor()
        self.file = open(filename, 'w')
        self.print_header()

        self.print_title('TODAY')
        self.cur.execute("select * from url where time > date('now','0 day') order by time desc")
        self.print_table()

        self.print_title('YESTERDAY')
        self.cur.execute("select * from url where time < date('now','0 day') and time > date('now','-1 day') order by time desc")
        self.print_table()

        self.print_title('TWO DAYS AGO')
        self.cur.execute("select * from url where time < date('now','-1 day') and time > date('now','-2 days') order by time desc")
        self.print_table()

        self.print_title('THREE DAYS AGO')
        self.cur.execute("select * from url where time < date('now','-2 day') and time > date('now','-3 days') order by time desc")
        self.print_table()

        self.print_footer()
        self.file.close()

    def print_row(self, (date, url, text, nick)):
        time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f" )
        timestr = str(time.strftime("%H:%M"))
        self.file.write("<tr>\n")
        self.file.write("    <td><p>%s</p></td>\n" % timestr)
        self.file.write("    <td><p>&lt;%s&gt;</p></td>\n" % nick)
        self.file.write("    <td><a href=\"%s\">%s</a></td>\n" % (url, text))
        self.file.write("</tr>\n")

    def print_title(self, text):
        self.file.write("<h3>"+text+"</h3>\n")

    def print_table(self):
        self.file.write("<table border=0>\n")
        for row in self.cur.fetchall():
            self.print_row(row)
        self.file.write("</table>\n")

    def print_header(self):
        self.file.write("<html>\n")
        self.file.write("<head><title>collected urls</title>\n")
        self.file.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head>\n")
        self.file.write("<body>\n")

    def print_footer(self):
        self.file.write("</body>\n")
        self.file.write("</html>\n")
