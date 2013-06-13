# -*- coding: utf-8 -*-
#!/usr/bin/python
# Onur Aslan <aslanon> <slnnronur@gmail.com> 
#
import os
import glob
from encrypt import Encrypt

path = os.getcwd()

desktopFile = glob.glob1(path, "*.desktop")
for dpFile in desktopFile:
  print "copying %s  --> /etc/xdg/autostart" % dpFile
  os.system("cp %s /etc/xdg/autostart" % dpFile)

pyFile = glob.glob1(path, "*.py")
for pyFile in pyFile:
  print "copying %s --> /usr/bin" % pyFile
  os.system("cp %s /usr/bin" % pyFile)

print "\nExample: /tmp/whoyou"
fileDirectory = raw_input("Work Directory:")

encryp = Encrypt()
password = raw_input("Your Mail Password:")
sifreli = encryp.xor(password)
print sifreli+"\n"

file = open("%s/key.txt" % fileDirectory, "w")
file.write(sifreli)
file.close()
print "Completed."