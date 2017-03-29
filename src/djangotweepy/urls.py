"""djangotweepy URL Configuration
"""

from django.conf.urls import *
from django.conf import settings

urlpatterns = [
    # redirect all urls to the twitter_auth app
    url(r'^', include('twitter_auth.urls')),
]
