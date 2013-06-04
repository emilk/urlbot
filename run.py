#!/usr/bin/python
import urlbot

HOST='irc.eagle.y.se'
PORT=6667
NICK='urlbot123'
IDENT='pybot'
REALNAME='s1ash'
CHANNEL='#testurltitle'

bot = urlbot.URLBot(HOST, PORT, NICK, IDENT, REALNAME, CHANNEL)
bot.run()
