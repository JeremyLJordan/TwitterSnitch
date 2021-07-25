from sys import argv
import tweepy
import smtplib
import sqlite3
from os.path import exists

  
# Twitter Authentication
access_token = #
access_token_secret = #
consumer_token = #
consumer_secret = #
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# End Authentication


#loads names,keywords and recipients
print "load twitter names: What is the file name? "
load_twit_usrs = raw_input("Press ENTER for default [twitUsrs.txt]") or "twitUsrs.txt"
if not ".txt" in load_twit_usrs: load_twit_usrs = load_twit_usrs + ".txt"
with open(load_twit_usrs) as f:
	nameList = [line.strip() for line in f]
	
print "load keywords: What is the file name? "
load_keywords = raw_input("Press ENTER for default [twitKeys.txt]") or "twitKeys.txt"
if not ".txt" in load_keywords: load_keywords = load_keywords + ".txt"
with open(load_keywords) as f:
	keywordList = [line.strip() for line in f]

print "load recipients: What is the file name? "
load_recipients = raw_input("Press ENTER for default [twitRecip.txt]") or "twitRecip.txt"
if not ".txt" in load_recipients: load_recipients = load_recipients + ".txt"
with open(load_recipients) as f:
	recipentList = [line.strip() for line in f]
#end loading

#get most recent tweet
def get_tweet(userIn):
	user = api.get_user(userIn)
	timeline = api.user_timeline(screen_name=userIn, count=1)
	for tweet in timeline:
		return tweet.text
#end get most recent tweet

def createdatabase(name, tweet, nameList):
	conn = sqlite3.connect('storedTweets.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS storedTweets(name TEXT, tweet TEXT)''')
	for names in nameList:
		c.execute("INSERT INTO storedTweets VALUES (?, ?)", name, tweet)
		conn.commit()
		conn.close()
		return names

#send mail
def send_Mail(recipentList, currentTweet, name):
	counter = 0
	username = 'walterblack1995@gmail.com'
	password = 'supersecretpassword'
	mailfrom = "walterblack1995@gmail.com"
	server = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
	server.ehlo()
	server.starttls()
	server.login(username, password)

	for recip in recipentList:
		print "made it to sendmail.recip %i" % (counter)
		mailto = recipentList[counter]
		subject = "Twitter Alert"
		body = ("User: %s " '\n' "Just Tweeted: %s" '\n' % (name, currentTweet))
		message = "\From: %s \nTo: %s\nSubject: %s\n\n%s" %(mailfrom, mailto, subject, body)
		#server.sendmail(mailfrom, mailto, message)
		counter += 1
#end send_Mail	

# process each name in list, pull last tweet, check for keywords, send email
def loopy(nameList):
	print "made it to loopy"
	for name in nameList:
		print "made it to for name"
		currentTweet = get_tweet(name).encode('utf-8')
		if any(word in currentTweet for word in keywordList):
			print "made it to any word in list"
			send_Mail(recipentList, currentTweet, name)
			createdatabase(name, currentTweet, nameList)				
#end process data

loopy(nameList)
