# -*- coding: utf-8 -*-

import commands

for i in range(67012,67014):
   print commands.getoutput("python iPeenCrawler.py " + str(i))
