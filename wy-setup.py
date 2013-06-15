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

encryp = Encrypt()
password = raw_input("Your Mail Password: ")
pwd = encryp.xor(password)
print pwd

print "\nTwitter status is read and command is sent to the computer\nTwitter Commands: PC:Close and PC:Open"
twitter_name = raw_input("Twitter Name: ")
twitter_file = open("%s/usernames" % fileDirectory, "w")
twitter_file.write("%s\n%s" % (mail, twitter_name))
twitter_file.close()

file = open("%s/wykey" % fileDirectory, "w")
file.write(pwd)
file.close()

user = os.listdir("/home/")
if user[0] != "samba":
  os.system("chown -R %s:users %s" % (user[0], fileDirectory))
  print "User:%s" % user[0]
else:
  os.system("chown -R %s:users %s" % (user[1], fileDirectory))
  print "User:%s" % user[1]

print "Completed."