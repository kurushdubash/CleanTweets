import twitter
import database
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

class TwitterUser():
	explicit_tweets = []
	alltweets = []
	tweets_deleted = 0
	explicit_tweets_non_objects = {}

	def __init__(self, token_key, token_secret, username):
		self.token_key = token_key
		self.token_secret = token_secret
		self.api = twitter.Api(consumer_key='5ZcYijaOIKQRVhfOqCsleC1uX',
	  				consumer_secret='IeZj8sLQiymNl1C3Tr1AagEUlFeAQIC73kiLelvGOP8cz5r8x9',
	  				access_token_key=str(token_key),
	  				access_token_secret=str(token_secret))
		self.username = username
		
		explicit_tweets_count = 0

		user_profile = self.api.GetUser(screen_name=username)

		self.user_public = True
		if user_profile.protected:
			self.user_public = False



	def get_all_tweets(self):
		"""
		   Returns a list of all possible tweets grabable for the specified user
		"""
		alltweets = []
		try:
			# get first 200 to start
			new_tweets = self.api.GetUserTimeline(screen_name=self.username, count=200)


			alltweets.extend(new_tweets)
			
			#save the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1

			#keep grabbing tweets until there are no tweets left to grab
			while len(new_tweets) > 0:
				print "Getting tweets with IDs before %s" % (oldest)
				
				#all subsiquent requests use the max_id param to prevent duplicates
				new_tweets = self.api.GetUserTimeline(screen_name=self.username, count=200, max_id=oldest)

				alltweets.extend(new_tweets)
				
				#update the id of the oldest tweet less one
				oldest = alltweets[-1].id - 1
				
				print "*** Downloaded " + str(len(alltweets)) + " tweets so far. " + str((len(alltweets) / 32) ) + "%" 
		except Exception as e:
			print e
		print "Finished download: 100%"
		return alltweets

	def is_tweet_bad(self, tweet):
		""" tweet : a Twitter Status object
			checks to see if the tweet contains any bad language referenced
			from our bad_words list
			Returns true if tweet contains bad word, false otherwise
		""" 
		text = tweet.text
		tweet_words = list(set(text.split()))
		ascii_tweet = self.strip_non_ascii(tweet_words)
		ascii_tweet = filter(None, ascii_tweet)
		for word in ascii_tweet:
			for item in bad_words:
				if word == item:
					return True
		return False

	def strip_non_ascii(self, list_of_words):
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

	def check_tweets(self, tweets):
		""" tweets : a list of Twitter Status objects
			goes through a list of twitter objects and checks to see if they are bad or not
		""" 
		bad_tweets = []
		for tweet in tweets:
			if self.is_tweet_bad(tweet):
				bad_tweets.append(tweet)
		return bad_tweets


	def get_twitter_embeds(self, tweets):
		""" Returns a list of all the explicit tweets in a web friendly embed for
		 	*** Requires check tweets to be before it
		"""
		tweets_in_embed_form = []
		try:
			for tweet in tweets:
				tweets_in_embed_form.append(self.api.GetStatusOembed(id=tweet.id))
			return tweets_in_embed_form
		except:
			return tweets_in_embed_form

	def clean_tweets(self):
		""" Looks at the list of twitter IDs in explict_tweet_ids and removes them.
		"""
		for tweet in self.explicit_tweets:
			self.api.DestroyStatus(tweet.id)
			print "Deleting Tweet: " + tweet.text + " : from " + tweet.relative_created_at + " : (" + tweet.created_at + ")"
			
		self.explicit_tweets = []
		self.explicit_tweets_non_objects = {}

	def get_bad_tweets(self):
		""" Returns a list of all the bad tweets
		"""
		self.alltweets = self.get_all_tweets()
		self.explicit_tweets = self.check_tweets(self.alltweets)
		self.explicit_tweets_non_objects = self.prepare_tweets_for_databse(self.explicit_tweets)
	
		self.explicit_tweets_count = len(self.explicit_tweets)
		return self.explicit_tweets

	def prepare_tweets_for_databse(self, twitter_objects):
		non_object_tweets = {}
		for tweet in self.explicit_tweets:
			non_object_tweets[tweet.id] = tweet.AsDict() 
		return non_object_tweets

	def update_database(self):
		database.add_user_to_database(self.username, self.explicit_tweets_non_objects)

	def post_tweets(self, text):
		self.api.PostUpdate(text)
		print "Posting tweet update: " + text

	def post_tweet(self, tweet_text):
		""" Posts tweet from user's account.
		"""
		self.api.PostUpdate(tweet_text)

# # For testing purposes
# user = get_user_object('kurushdubash')

# tweets = get_all_tweets(user)
# check_tweets(tweets)
# get_twitter_embeds()
# clean_tweets()

