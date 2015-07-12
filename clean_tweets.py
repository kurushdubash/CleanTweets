import twitter
from string import ascii_letters
from bad_words import bad_words # Gets a list of all the bad words

# auth stuff for testing purposes
api = twitter.Api(consumer_key='VzoDn3WeXht6OkS2HvNueflzL',
	  consumer_secret='wAmFnCv4w3o5dV4gBSzCTTJbMaDaUWoMKBrRPesljECUPJMzKW',
	  access_token_key='46310347-WAJLn4UDyfxlupMy7Q1nNoyQ4F4OpjZdjaVCPtCGJ',
	  access_token_secret='FObEKM6jMrYX884j8TlzoywREW5fI1A7ZfSQFa8xY41AB')

# # for production
# api = twitter.Apit(consumer_key=consumer_key, 
# 					  consumer_secret=consumer_secret, 
# 					  access_token_key=access_token_key, 
# 					  access_token_secret=access_token_secret)

explicit_tweets = [] # a list of twitter status objects that we coined as 'bad'

def get_auth_info(consumer_key, consumer_secret, access_token_key, access_token_secret):
	""" Takes in consumer_key, consumer_secret, access_token_key, access_token_secret
		from user input
		Returns respective values
	"""	
	return consumer_key, consumer_secret, access_token_key, access_token_secret

def get_user_object(username):
	""" username: a string of the username we want to create an object for.
		Returns a twitter user object based on the inputed username.
	"""
	return api.GetUser(screen_name=username)

def get_tweets(user):
	""" user : a Twitter user object
		Returns a list of tweets for the specified user 
	"""
	return api.GetUserTimeline(screen_name=user.screen_name, count=10)

def is_tweet_bad(tweet):
	""" tweet : a Twitter Status object
		checks to see if the tweet contains any bad language referenced
		from our bad_words list
		Returns true if tweet contains bad word, false otherwise
	""" 
	text = tweet.text
	tweet_words = list(set(text.split()))
	ascii_tweet = strip_non_ascii(tweet_words)
	ascii_tweet = filter(None, ascii_tweet)
	for word in ascii_tweet:
		if word in bad_words:
			return True
	return False

def strip_non_ascii(list_of_words):
	""" tweets : a list of 
		cleans the words to remove non-ascii characters
		returns a list of cleaned words
	"""
	words = []
	count = 0
	while (count < len(list_of_words)):
		word = ''
		for char in list_of_words[count]:
			if char in ascii_letters: # if the character is an ascii char digit, add it to our word
				word += char
			else:
				words.append(word)
				word = ''
		words.append(word)
		count+=1
	return words

def check_tweets(tweets):
	""" tweets : a list of Twitter Status objects
		goes through a list of twitter objects and checks to see if they are bad or not
	""" 
	for tweet in tweets:
		if is_tweet_bad(tweet):
			explicit_tweets.append(tweet)
			
def clean_tweets():
	""" Looks at the list of twitter IDs in explict_tweet_ids and removes them.
	"""
	for tweet in explicit_tweets:
		api.DestroyStatus(tweet.id)
		print "Deleting Tweet: " + tweet.text
		explicit_tweets.remove(tweet)

# For testing purposes
user = get_user_object('kurushdubash')
tweets= get_tweets(user)
check_tweets(tweets)
clean_tweets()