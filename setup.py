import os
print "copying whoyou.py --> /usr/bin"
os.system("cp whoyou.py /usr/bin")
print "copying whoyou.desktop  --> /etc/xdg/autostart"
os.system("cp whoyou.desktop /etc/xdg/autostart")