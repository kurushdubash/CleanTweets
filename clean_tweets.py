import twitter
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
	return consumer_key, consumer_secret, access_token_key, access_token_secret

def get_user_object(username):
	""" username: a string of the username we want to create an object for.
		Returns a twitter user object based on the inputed username.
	"""
	return api.GetUser(screen_name=username)


def clean_tweets():
	""" Looks at the list of twitter IDs in explict_tweet_ids and removes them.
	"""
	for tweet in explicit_tweets:
		api.DestroyStatus(tweet.id)
		print "Deleting Tweet: " + tweet.text
		explicit_tweets.remove(tweet)