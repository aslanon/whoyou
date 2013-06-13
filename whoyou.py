# -*- coding: utf-8 -*-
#!/usr/bin/python
# Onur Aslan <aslanon> <slnnronur@gmail.com> 
#
# python-v4l2capture
#

import os, sys
import glob
import operator
import urllib
import Image
import select
import time
import v4l2capture
import gtk.gdk
import locale
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from encrypt import Encrypt

locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
TIME = time.strftime("%X")
DATE = time.strftime("%d.%m.%Y")
DATETIME = DATE, TIME  

MINUTE = int("5")
AMOUNT = int("2")
fileDirectory = "/tmp/whoyou"
VIDEO_X = "video0"
VALUEURL = "http://whoyou.googlecode.com/svn/value" # if value == 0: pc shutdown. elif value == 1: pc open



encryp = Encrypt()
key = open("%s/key.txt" % fileDirectory).read()
openPass = encryp.xor(key, False)
MAIL_PASSWORD = encryp.decrypt(openPass)



MAIL = "slnnronur@gmail.com"
SUBJECT = "-*-whoyou-*-"


TEXT = """
Merhaba %s,\n%s tarhinde sisteminize giriş yapıldı. 
Bilgisayarınız ile ilgili işlem yapmak için verdiğiniz adrese (%s) bir değer giriniz. Aksi halde bilgisayarınız açık kalacaktır.
İlgili görsellere "%s" dizininden bakabilirsiniz.""" % (MAIL.split("@")[0], DATETIME, VALUEURL, fileDirectory)
  

if os.path.isdir(fileDirectory) == True:
  pass
else:
  os.mkdir(fileDirectory)

FILES = glob.glob1(fileDirectory, "*.*g")
 
 
def interval(minute, amount):
  print """\n
#################################################################
## whoyou a Aslanon product. ##  http://aslanonur.blogspot.com ##
#################################################################
             ## < slnnronur@gmail.com > ##
             #############################
"""
  global TIME, DATE, DATETIME
  value = 0
  for no in range(0, amount):
    time.sleep(minute)
    TIME = time.strftime("%X")
    DATE = time.strftime("%d.%m.%Y")
    DATETIME = DATE, TIME      
    value += 1
    __takePhoto("photo_%s" % value, DATETIME)    
    __takeScreenshot("ss_%s" % value, DATETIME) 
    __readValue()
    
  __reportSend(MAIL, SUBJECT, TEXT, FILES)    
  print "Closed..."
  sys.exit()
    
def __readValue():
    urlValue = urllib.urlopen(VALUEURL).read()
    valueFile = open("%s/value.txt" % fileDirectory, "wb")
    valueFile.write(urlValue)
    valueFile.close()
    value = file("%s/value.txt" % fileDirectory).read()
    if value == "0":
        print "Value = 0: PC closing...\n"
    else:
        print "Value = 1: PC free...\n"

def __reportSend(mail, subject, text, attach):
   msg = MIMEMultipart()
   msg['From'] = MAIL
   msg['To'] = MAIL
   msg['Subject'] = subject
   msg.attach(MIMEText(text))
    
   for files in FILES:
     file = "%s/%s" % (fileDirectory, files)
     if files != "":
       part = MIMEBase('application', 'octet-stream')
       part.set_payload(open(file, 'rb').read())
       Encoders.encode_base64(part)
       part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(files))
       msg.attach(part)
     else:
       pass
   
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(MAIL, MAIL_PASSWORD)
   mailServer.sendmail(MAIL, mail, msg.as_string())
   mailServer.close()
   print "E-mail has been sent.\n"

def __takePhoto(photoName, dateTime):
  video = v4l2capture.Video_device("/dev/%s" % VIDEO_X)
  size_x, size_y = video.set_format(640, 480)
  video.create_buffers(1)
  video.start()
  time.sleep(3)
  video.queue_all_buffers()
  select.select((video,), (), ())
  image_data = video.read()
  video.close()
  image = Image.fromstring("RGB", (size_x, size_y), image_data)
  image.save("%s/%s.jpg" % (fileDirectory, photoName))
  print "%s | Taked photo: %s/%s.jpg" % (dateTime, fileDirectory,photoName)
  
def __takeScreenshot(ssName, dateTime):
  main = gtk.gdk.get_default_root_window()
  size = main.get_size()
  take = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, size[0], size[1])
  take = take.get_from_drawable(main, main.get_colormap(), 0, 0, 0, 0, size[0], size[1])
  if take != None:
    take.save("%s/%s.png" % (fileDirectory, ssName), "png")
    print "%s | Taked screenshot: %s/%s.png" % (dateTime, fileDirectory, ssName)
  else:
    print "Failed: its not take screenshot"
    
interval(MINUTE, AMOUNT) 


#Sifreleme kodları kaynak: http://pythontr.blogspot.com/2008/09/ev-yapm-ifreleme.html
#Teşekkürler PythonTr ve Aydın Şen

class Encrypt():
 def xor(self, password,encrypt=True):
    key=self.mix_mac()
    if not encrypt:
      key+='\x00'
    p_sira = -1
    encrypted = ""
    for str_sira in range(len(key)):
       p_sira += 1
       if (p_sira >= len(password)): p_sira = 0
       p = str(password[p_sira])
       s = str(key[str_sira])
       e = chr ( operator.xor(ord(s), ord(p)))
       encrypted += e
    if encrypt:
      encrypted += str(len(password))
    return encrypted

 def decrypt(self,enc):
    enc_len=int(enc[len(enc)-1])
    return enc[:enc_len]

 def mix_mac(self):
    mac=self.getMacAddress()
    KEY='pythontr'
    mixed_mac=''
    str_mac=str(mac)
  
    for i in range(len(KEY)):
       mixed_mac+=str_mac[i]+KEY[i]
       mixed_mac+=str_mac[len(KEY):]
    return mixed_mac
 
 def getMacAddress(self):
    if sys.platform == 'win32':
       for line in os.popen("ipconfig /all"):
           if line.lstrip().startswith('Physical Address'):
              mac = line.split(':')[1].strip().replace('-',':')
              break
    else:
       for line in os.popen("/sbin/ifconfig"):
          if line.find('Ether') > -1:
             mac = line.split()[4]
             break
    return mac