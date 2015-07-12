from flask import Flask
from flask import render_template
from flask_oauth import OAuth
from flask import session, redirect, url_for, flash, request

app = Flask(__name__)
app.secret_key="testingkey"
oauth = OAuth()
twitter = oauth.remote_app('twitter',
base_url='https://api.twitter.com/1/',
request_token_url='https://api.twitter.com/oauth/request_token',
access_token_url='https://api.twitter.com/oauth/access_token',
authorize_url='https://api.twitter.com/oauth/authenticate',
consumer_key='VzoDn3WeXht6OkS2HvNueflzL',
consumer_secret='wAmFnCv4w3o5dV4gBSzCTTJbMaDaUWoMKBrRPesljECUPJMzKW')
#consumer_key='xBeXxg9lyElUgwZT6AZ0A',
#consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk')

@app.route("/")
def hello():
    return render_template('sign_in.html')

@app.route("/hello/")
def help_page(name=None):
	return render_template('hello_world.html')

@app.route("/login")
def login():	
	return twitter.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

## EXAMPLE ON USING ON-THE-FLY URLS
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)