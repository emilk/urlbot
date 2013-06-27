#!/usr/bin/python
# -*- coding: utf-8 -*-

import urldescription


desc  = urldescription.URLdescription()

'''
url   = 'http://www.eurogamer.net/articles/2013-06-26-microsoft-no-longer-charges-developers-to-patch-their-xbox-360-games'
title = desc.fetchtitle(url)
print 'Title: ', title
title = desc.unescape(title)
print 'Title: ', title
'''

print "Bullet: |" + desc.unescape('&lt;_&#8226;_&quot;_&apos;_&amp;_&copy;_&#65;_&gt;') + "|"

#print unicode('Some unicode: åäö, Ϟ Ϡ Ϣ ϣ ಂ ಃ ಅ ಆ ಇ ಈ ಉ ಊ')
#print '\ua000'
