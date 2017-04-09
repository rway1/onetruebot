#!/usr/bin/python3.5

import praw
import time
import re
import os
import subprocess
from pprint import pprint

regex = re.compile(r"((N|n)(ic(h|)olas|ick) (C|c)age)")
sleep_time_regex = re.compile('\d')

def m_sleep(m_time):
    os.system("date")
    time.sleep(m_time)

def generateReply():
  return (subprocess.check_output(
      "shuf ~/OneTrueGodBot/phrases | head -n 1",
      shell=True
    ) +
    subprocess.check_output(
      "shuf ~/OneTrueGodBot/pics_file | head -n 1",
      shell=True
    ))

def alreadyReply(comments):
  for comment in comments:
    if((comment.author) and (comment.author.name == 'OneTrueGodBot')):
      return True
  return False

def findComments(comments):
  found = []
  for comment in comments:
    if(re.search(regex, comment.body)
      and not alreadyReply(comment.replies)):
      found.append(comment)
  return found

  


while 1:
  #subreddit = r.subreddit('OneTrueGodBotTesting')
  #for subreddit in r.subreddits.default(limit=None):
  #  for submission in subreddit.top(limit=30):
  r = praw.Reddit('onetruegod',
    username='OneTrueGodBot',
    password='flounder922',
    user_agent='none')
  subreddit = r.subreddit('all')
  for submission in subreddit.search('Nicolas Cage', sort='new', limit=25):
    roots = []
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
      if(comment.is_root):
        roots.append(comment)
    if(not alreadyReply(roots)):
      try:
        submission.reply(generateReply())
        print(submission.title)
      except praw.exceptions.APIException as error:
        m_sleep(int(re.search(sleep_time_regex, error.message).group(0))*60)
  for comment in subreddit.comments(limit=None):
    if(re.search(regex, comment.body) and not
      alreadyReply(comment.replies.list())):
      try:
        comment.reply(generateReply())
        print("replied to comment\n")
      except praw.exceptions.APIException as error:
        m_sleep(int(re.search(sleep_time_regex, error.message).group(0))*60)
  m_sleep(10)
