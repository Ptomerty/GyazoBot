import praw
import requests
from requests.exceptions import HTTPError

reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')

allsubs = reddit.subreddit('ZXhwb3NlX2tyZXNfYmFv')
reply_template = ('Hi, I\'m a bot that directly links Gyazo images.'
                  '\n\n{}\n\n'
                  '^^[Creator](https://reddit.com/u/derpherp128)')


def check_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except HTTPError:
        print('HTTP Error!')
        return False
    else:
        print('Success!')
        return True

def process(submission, url):
    if "gyazo.com" in url and "i.gyazo.com" not in url:
        split_arr = url.split("/")
        print(split_arr)
        if len(split_arr) >= 4:
            gyazo_id = split_arr[3]  # it's an actual gyazo image
            fixed_url = 'https://i.gyazo.com/' + gyazo_id + '.png'
            print(fixed_url)
            if check_url(fixed_url):
                print('png okay')
                reply_text = reply_template.format(fixed_url)
                submission.reply(reply_text)
            elif check_url(fixed_url[:-3] + 'jpg'):
                fixed_url = fixed_url[:-3] + 'jpg'
                print('jpg okay')
                reply_text = reply_template.format(fixed_url)
                submission.reply(reply_text)

def main():
    for submission in allsubs.stream.submissions():
        process(submission, submission.url)

if __name__ == '__main__':
    main()



