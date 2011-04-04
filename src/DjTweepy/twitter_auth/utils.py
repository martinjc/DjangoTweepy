import tweepy

CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'

def get_api(request):
	# set up and return a twitter api object
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api