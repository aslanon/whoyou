import urllib, re

twitter_status = True
twitter_command = ""

fileDirectory = "/tmp/whoyou"

tweet_user = open("%s/usernames" % fileDirectory).readlines()[1]

twitter = urllib.urlopen("http://twitter.com/%s" % tweet_user)
twitterCompile = re.compile('<p class="js-tweet-text tweet-text">(.+?)</p>')
tweet_text = twitterCompile.findall(twitter.read())
print "Tweet Command:", "'"+tweet_text[0]+"'"

if tweet_text[0] == "PC:Close":
  twitter_command = "Close"
  print "Closing..."
elif tweet_text[0] == "PC:Open":
  twitter_command = "Open"
  print "Open..."
else:
  twitter_status = False
  print "Invalid tweet."
  
#print twitter_status, twitter_command