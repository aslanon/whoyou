# -*- coding: utf-8 -*-
#!/usr/bin/python
# Onur Aslan <aslanon> <slnnronur@gmail.com> 
#
import os
import glob
from encrypt import Encrypt

path = os.getcwd()

fileDirectory = "/tmp/whoyou"
if os.path.exists(fileDirectory) == False:
  os.mkdir(fileDirectory)
  print "Created Work Dir: %s" % fileDirectory
else:
  print "Work Dir: %s" % fileDirectory
desktopFile = glob.glob1(path, "*.desktop")
for dpFile in desktopFile:
  print "copying %s  --> /etc/xdg/autostart" % dpFile
  os.system("cp %s /etc/xdg/autostart" % dpFile)

pyFile = glob.glob1(path, "*.py")
for pyFile in pyFile:
  print "copying %s --> /usr/bin" % pyFile
  os.system("cp %s /usr/bin" % pyFile)

mail = raw_input("Your Mail: ")
mailFile = open("%s/wy-mail.txt" % fileDirectory, "w")
mailFile.write(mail)
mailFile.close()

encryp = Encrypt()
password = raw_input("Your Mail Password: ")
pwd = encryp.xor(password)
print pwd

file = open("%s/key.txt" % fileDirectory, "w")
file.write(pwd)
file.close()
print "Completed."