"""Config vars"""
import os
from apiclient.discovery import build

PRAW_SECRET = os.environ.get('', None)
PRAW_KEY = os.environ.get('', None)
PRAW_USER_AGENT = os.environ.get('', None)

SUBREDDITS = [
    "Coronavirus",
"CoronavirusFOS",
"CoronavirusNewYork",
"CoronavirusCA",
"CoronavirusUK",
"nCoV",
"CoronavirusUS",
"CoronaVirus_2019_nCoV"]


