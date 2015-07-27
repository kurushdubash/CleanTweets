from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
import clean_tweets


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='5ZcYijaOIKQRVhfOqCsleC1uX',
    consumer_secret='IeZj8sLQiymNl1C3Tr1AagEUlFeAQIC73kiLelvGOP8cz5r8x9',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

User = None
freshly_cleaned = False

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


@app.route('/')
def index():
    tweets_embed = None
    bad_tweets = None
    user_public = None
    global freshly_cleaned
    if g.user is not None and not freshly_cleaned:
        outh_token, outh_secret = get_twitter_token()
        username = g.user["screen_name"]

        global User
        User = clean_tweets.TwitterUser(outh_token, outh_secret, username)

        bad_tweets = User.get_bad_tweets()
        tweets_embed = User.get_twitter_embeds(bad_tweets)
        User.update_database()
        user_public = User.user_public
    else:
        flash('Unable to load tweets from Twitter. You may have just cleaned your twitter')
        global freshly_cleaned
        freshly_cleaned = False
    return render_template('index.html', tweets_embed=tweets_embed, dirty_tweets=bad_tweets, user_public=user_public)


@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    print resp
    return redirect(url_for('index'))


@app.route('/cleanMyDirtyTweets')
def cleanMyDirtyTweets():
    User.clean_tweets()
    global freshly_cleaned
    freshly_cleaned = True
    User.post_tweet('CleanTweets helped me remove {0} of my Dirty Tweets! Visit www.CleanTweets.me to remove all your inappropriate and explicit Tweets!'.format(User.explicit_tweets_count))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
