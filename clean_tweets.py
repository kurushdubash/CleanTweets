import requests
import twitter
import os

# global var for bad words
bad_words = []

# auth stuff
api = twitter.Api(consumer_key='VzoDn3WeXht6OkS2HvNueflzL',
                      consumer_secret='wAmFnCv4w3o5dV4gBSzCTTJbMaDaUWoMKBrRPesljECUPJMzKW',
                      access_token_key='46310347-WAJLn4UDyfxlupMy7Q1nNoyQ4F4OpjZdjaVCPtCGJ',
                      access_token_secret='FObEKM6jMrYX884j8TlzoywREW5fI1A7ZfSQFa8xY41AB')

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