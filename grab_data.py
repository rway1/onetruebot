#!/usr/bin/python3.5

import time
import praw
import urllib
import subprocess

from urllib import request
from urllib.request import urlopen
from io import StringIO
from path import Path
from pprint import pprint

img_dir = Path("/home/rway/OneTrueGodBot/pics_file")
_image_formats = ['gif','jpg','jpeg','png']

def is_image_link(submission):
	if (submission.subreddit.display_name == 'OneTrueGod' or 
	'imgur' in submission.domain.split('.') or 
	submission.url.split('.')[-1] in _image_formats):
		return True
	else:
		return False


r = praw.Reddit('onetruegod', user_agent='OneTrueGodBot')
subreddit = r.subreddit('Onetruegod')

for submission in subreddit.hot(limit=None):
	if is_image_link(submission):
		response = urllib.request.urlopen(submission.url)
		data = response.read()

		with open(img_dir, "a") as pic:
			pic.write(submission.url)
			pic.write("\n")
			print("Added new picture")
		pic.close()
		subprocess.check_output("sort pics_file | uniq -u", shell=True)
		time.sleep(600)
	
