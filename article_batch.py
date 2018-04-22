# -*- coding: utf-8 -*-

import commands

for i in range(67012,67014):
    for j in range(1, 3):
        output = commands.getoutput("python article.py " + str(i) + " " + str(j))
        print output
        if "There are no articles in the page:" in output:
            print "The restaurant ID = " + str(i) + ", page = " + str(j) + " is no data.........."
            break
