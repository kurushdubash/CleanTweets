import twitter
from string import ascii_letters
from bad_words import bad_words # Gets a list of all the bad words

# auth stuff for testing purposes
# api = twitter.Api(consumer_key='5ZcYijaOIKQRVhfOqCsleC1uX',
# 	  consumer_secret='IeZj8sLQiymNl1C3Tr1AagEUlFeAQIC73kiLelvGOP8cz5r8x9',
# 	  access_token_key='29823087-wyFqsOIbfVwomSM7O5jca4e4i00Kqcisw7NeDvKIc',
# 	  access_token_secret='KASM0GiD4wZXzxJqO4hH2nHXwX5BpDOywstZvvYKDPt7g')

# # for production
# api = twitter.Api(consumer_key=consumer_key, 
# 					  consumer_secret=consumer_secret, 
# 					  access_token_key=access_token_key, 
# 					  access_token_secret=access_token_secret)

# explicit_tweets = [] # a list of twitter status objects that we coined as 'bad'

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
		Returns a list of the 200 most recent tweets for the specified user 
	"""
	return api.GetUserTimeline(screen_name=user.screen_name, count=200)

def get_all_tweets(user):
	"""
	   user : a Twitter user object
	   Returns a list of all possible tweets grabable for the specified user
	"""
	alltweets = []
	try:
		# get first 200 to start
		new_tweets = get_tweets(user)


		alltweets.extend(new_tweets)
		
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print "Getting tweets with IDs before %s" % (oldest)
			
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.GetUserTimeline(screen_name=user.screen_name, count=200, max_id=oldest)

			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			print "*** Downloaded " + str(len(alltweets)) + " tweets so far. " + str((len(alltweets) / 32) ) + "%" 
	except Exception as e:
		print e
	print "Finished download: 100%"
	return alltweets


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

def check_tweets(tweets, explicit_tweets):
	""" tweets : a list of Twitter Status objects
		goes through a list of twitter objects and checks to see if they are bad or not
	""" 
	for tweet in tweets:
		if is_tweet_bad(tweet):
			explicit_tweets.append(tweet)


def get_twitter_embeds(api, explicit_tweets):
	""" Returns a list of all the explicit tweets in a web friendly embed for
	 	*** Requires check tweets to be before it
	"""
	tweets_in_embed_form = []
	for tweet in explicit_tweets:
		tweets_in_embed_form.append(api.GetStatusOembed(id=tweet.id))
	return tweets_in_embed_form

def clean_tweets():
	""" Looks at the list of twitter IDs in explict_tweet_ids and removes them.
	"""

	for tweet in explicit_tweets:
		api.DestroyStatus(tweet.id)
		print "Deleting Tweet: " + tweet.text + " : from " + tweet.relative_created_at + " : (" + tweet.created_at + ")"
		explicit_tweets.remove(tweet)

def doItAll(username, token_key, token_secret):
	api = twitter.Api(consumer_key='5ZcYijaOIKQRVhfOqCsleC1uX',
	  consumer_secret='IeZj8sLQiymNl1C3Tr1AagEUlFeAQIC73kiLelvGOP8cz5r8x9',
	  access_token_key=str(token_key),
	  access_token_secret=str(token_secret))
	explicit_tweets = [] # a list of twitter status objects that we coined as 'bad'

	user = api.GetUser(screen_name=username)
	tweets = api.GetUserTimeline(screen_name=user.screen_name, count=200)
	check_tweets(tweets, explicit_tweets)
	# tweets_array = get_twitter_embeds(api, explicit_tweets)
	# print tweets_array
	return explicit_tweets



# # For testing purposes
# user = get_user_object('kurushdubash')

# tweets = get_all_tweets(user)
# check_tweets(tweets)
# get_twitter_embeds()
# clean_tweets()

