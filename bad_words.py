import os
def get_bad_words():
	""" Finds all the bad words from a local directory and puts it into our 
		global variable "bad_words" list
	"""
	words = []
	sub_dir = 'bad_words_multiple_languages' # sub directory name
	for filename in os.listdir(sub_dir): # for each file in our sub directory
		if filename == "en": # for testing purposes we'll only work with english words
		    with open(os.path.join(sub_dir, filename), "r") as f:
		        for line in f:
		        	word = line[: len(line) - 1]
		        	words.append(word)
	return words

bad_words = get_bad_words()