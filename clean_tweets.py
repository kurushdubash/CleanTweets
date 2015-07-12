import twitter
import os

# auth stuff for testing purposes
api = twitter.Api(consumer_key='VzoDn3WeXht6OkS2HvNueflzL',
                      consumer_secret='wAmFnCv4w3o5dV4gBSzCTTJbMaDaUWoMKBrRPesljECUPJMzKW',
                      access_token_key='46310347-WAJLn4UDyfxlupMy7Q1nNoyQ4F4OpjZdjaVCPtCGJ',
                      access_token_secret='FObEKM6jMrYX884j8TlzoywREW5fI1A7ZfSQFa8xY41AB')


# global var for bad words
bad_words = []
explict_tweet_ids = [] 

def get_auth_info(consumer_key, consumer_secret, access_token_key, access_token_secret):
	return consumer_key, consumer_secret, access_token_key, access_token_secret

def get_user_object(username):
	""" username: a string of the username we want to create an object for.
		Returns a twitter user object based on the inputed username.
	"""
	return api.GetUser(screen_name=username)

# # for production
# api = twitter.Apit(consumer_key=consumer_key, 
# 					  consumer_secret=consumer_secret, 
# 					  access_token_key=access_token_key, 
# 					  access_token_secret=access_token_secret)


def get_bad_words():
	""" Finds all the bad words from a local directory and puts it into our 
		global variable "bad_words" list
	"""
	sub_dir = 'bad_words' # sub directory name
	for filename in os.listdir(sub_dir): # for each file in our sub directory
		if filename == "en": # for testing purposes we'll only work with english words
		    with open(os.path.join(sub_dir, filename), "r") as f:
		        for line in f:
		        	word = line[: len(line) - 1]
		        	bad_words.append(word)

get_bad_words()


