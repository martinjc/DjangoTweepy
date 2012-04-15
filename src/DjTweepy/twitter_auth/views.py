# Create your views here.
import tweepy
from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from utils import *

def main(request):
	"""
	main view of app, either login page or info page
	"""
	# if we haven't authorised yet, direct to login page
	if check_key(request):
		return HttpResponseRedirect(reverse('info'))
	else:
		return render_to_response('twitter_auth/login.html')
 
def unauth(request):
	"""
	logout and remove all session data
	"""
	if check_key(request):
		api = get_api(request)
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('main'))

def info(request):
	"""
	display some user info to show we have authenticated successfully
	"""
	if check_key(request):
		api = get_api(request)
		user = api.me()
		return render_to_response('twitter_auth/info.html', {'user' : user})
	else:
		return HttpResponseRedirect(reverse('main'))

def auth(request):
	# start the OAuth process, set up a handler with our details
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['unauthed_token_tw'] = (oauth.request_token.key, oauth.request_token.secret) 
    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    oauth.set_request_token(token[0], token[1])
    # get the access token and store
    try:
    	oauth.get_access_token(verifier)
    except tweepy.TweepError:
    	print 'Error, failed to get access token'
    request.session['access_key_tw'] = oauth.access_token.key
    request.session['access_secret_tw'] = oauth.access_token.secret
    response = HttpResponseRedirect(reverse('info'))
    return response

def check_key(request):
	"""
	Check to see if we already have an access_key stored, if we do then we have already gone through 
	OAuth. If not then we haven't and we probably need to.
	"""
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True