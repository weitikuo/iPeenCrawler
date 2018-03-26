# -*- coding: utf-8 -*-

import commands

for i in range(67012,67020):
   print commands.getoutput("python iPeenCrawler.py " + str(i))

