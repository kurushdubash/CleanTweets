from firebase import firebase
firebase = firebase.FirebaseApplication('https://cleantweets.firebaseio.com/', None)


def does_user_exist(username):
	""" Checks to see if a user already exists in the database, if so return true
	"""
	if firebase.get('Users/' + username, None):
		return True
	return False

def add_user_to_database(username, data):
	""" username  = the user name of the person
		data = a dict of all the explicit tweets
	"""
	if does_user_exist(username):
		existing_data =  firebase.get('Users/' + username, None)
		data = merge_two_dicts(data, existing_data)
	firebase.put('/Users', name=username, data=data)

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z