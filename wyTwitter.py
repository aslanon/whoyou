import urllib, re, os
  
  
twitter_status = True
twitter_command = ""

fileDirectory = "/tmp/whoyou"

tweet_user = open("%s/usernames" % fileDirectory).readlines()[1]

twitter = urllib.urlopen("http://twitter.com/%s" % tweet_user)
twitterCompile = re.compile('<p class="js-tweet-text tweet-text">(.+?)</p>')
tweet_text = twitterCompile.findall(twitter.read())
print "Tweet Command:", "'"+tweet_text[0]+"'"

if os.path.isfile("%s/command" % fileDirectory) == False:
  file = open("%s/command" % fileDirectory, "w")
  file.write("open")
  file.close()    

if tweet_text[0] == "PC:Close":
  twitter_status = True
  twitter_command = "Close"
  file = open("%s/command" % fileDirectory, "w")
  file.write("close")
  file.close()
  print "Closing..."
  os.system("qdbus org.kde.ksmserver /KSMServer logout 0 2 0")
  
elif tweet_text[0] == "PC:Open":
  twitter_status = True    
  twitter_command = "Open"
  file =open("%s/command" % fileDirectory,"w")
  file.write("open")
  file.close()
  print "Open..."
  
else:
  twitter_status = False
  twitter_command = False
  print "Invalid tweet."
  file =open("%s/command" % fileDirectory).read()
  if file == "close":
    print "Closing..."
    os.system("qdbus org.kde.ksmserver /KSMServer logout 0 2 0")
  elif file == "open":
    print "Open..."
  
print "Twitter Status:", twitter_status, "Twitter Command:", twitter_command