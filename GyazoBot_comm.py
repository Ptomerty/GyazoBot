import praw
import requests
import re
from requests.exceptions import *

reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')

regex = '(?<!\w\.)gyazo\.com/\w{32}'

allsubs = reddit.subreddit('all')
reply_template_header = ('Hi, I\'m a bot that links Gyazo images directly.\n\n')

reply_template_footer = ( '^^[Source](https://github.com/Ptomerty/GyazoBot) ^^| '
                  '^^[Why?](https://github.com/Ptomerty/GyazoBot/blob/master/README.md) ^^| '
                  '^^[Creator](https://reddit.com/u/derpherp128)')

def check_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except : #catch all HTTP errors
        return False
    else:
        return True

def process(url):
        print(url[10:])
        gyazo_id = url[10:]
        fixed_url = 'https://i.gyazo.com/' + gyazo_id + '.png'
        if check_url(fixed_url):
            #print('png okay')
            return fixed_url
        elif check_url(fixed_url[:-3] + 'jpg'):
            fixed_url = fixed_url[:-3] + 'jpg'
            #print('jpg okay')
            return fixed_url
        else:
            return ''

def main():
    for comment in allsubs.stream.comments():
        list = re.findall(regex,comment.body)
        if (list):
            a = reply_template_header
            for url in list:
                fixed = process(url)
                if (fixed != ''):
                    a += process(url) + '\n\n'
            if (a != reply_template_header): #make sure there's an actual fixed link
                a += reply_template_footer
                comment.reply(a)


if __name__ == '__main__':
    main()



