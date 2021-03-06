import praw
import praw.exceptions
import requests
import requests.exceptions
import os
import time
import sys
import configparser

from imgurpython import ImgurClient

ignore = []
mtime = 0

def check_url(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except:  # catch all HTTP errors
        return False
    else:
        return True


def process(submission):
    url = submission.url
    if "gyazo.com" in url and "i.gyazo.com" not in url:
        split_arr = url.split("/")
        if len(split_arr) >= 4:
            gyazo_id = split_arr[3]  # it's an actual gyazo image
            fixed_url = 'https://i.gyazo.com/' + gyazo_id + ".png"
            if check_url(fixed_url):
                # print('png okay')
                return fixed_url
            elif check_url(fixed_url[:-3] + "jpg"):
                return fixed_url[:-3] + "jpg"
            elif check_url(fixed_url[:-3] + "mp4"):
                return fixed_url[:-3] + "mp4"
            else:
                return ''


def refreshIgnore():
    global ignore
    global mtime
    if os.path.isfile("./ignore") and os.path.getmtime("./ignore") != mtime:
        with open("./ignore", "r") as f:
            for line in f:
                item = line.split("\n")[0]
                if item not in ignore:
                    ignore.append(item)
        mtime = os.path.getmtime("./ignore")


def main():
    reply_template = ('Hi, I\'m a bot that links Gyazo images directly to save bandwidth.'
                      '\n\nDirect link: {}\n\nImgur mirror: {}\n\n'
                      '^^[Sourcev2](https://github.com/Ptomerty/GyazoBot) ^^| '
                      '^^[Why?](https://github.com/Ptomerty/GyazoBot/blob/master/README.md) ^^| '
                      '^^[Creator](https://np.reddit.com/u/derpherp128) ^^| '
                      '^^[leavemealone](https://np.reddit.com/message/compose/?to=Gyazo_Bot'
                      '&subject=ignoreme&message=ignoreme)')
    global ignore
    posts = []

    refreshIgnore()

    if os.path.isfile("./posts"):
        with open("./posts", "r") as f:
            for line in f:
                posts.append(line.split("\n")[0])

    config = configparser.ConfigParser()
    config.read('auth.ini')
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    client = ImgurClient(client_id, client_secret)
    print('imgur client launched')

    reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')
    print('reddit client launched')

    while True:
        print('starting bot')
        try:
            for submission in reddit.subreddit('all').stream.submissions():
                refreshIgnore()
                if not submission.author in ignore and not submission.id in posts:
                    fixed = process(submission)
                    if fixed is not '' and fixed is not None and fixed not in submission.url:
                        link = process(submission)
                        imgurlink = client.upload_from_url(link)['link']
                        reply_text = reply_template.format(link, imgurlink)
                        try:
                            submission.reply(reply_text)
                            posts.append(submission.id)
                            with open("./postlog", "a+") as cmtfs:
                                cmtfs.write('{0}\n'.format(submission.id))
                                cmtfs.write('{0}\n'.format(submission.url))
                                cmtfs.flush()
                                os.fsync(cmtfs.fileno())
                            with open("./posts", "a+") as postfs:
                                postfs.write('{0}\n'.format(submission.id))
                                postfs.flush()
                                os.fsync(postfs.fileno())
                        except praw.exceptions.APIException:
                                time.sleep(60 * 10)  # ratelimit hit
                        except requests.exceptions.ReadTimeout:
                            # misc timeout
                            print("timeout error")
                            pass
                        except Exception as e:
                            print(e)
        except requests.exceptions.ReadTimeout:
            # misc timeout
            print("timeout error")
            pass
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
