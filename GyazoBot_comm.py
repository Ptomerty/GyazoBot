import praw
import requests
import re
import os

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


def process(url):
    gyazo_id = url[10:]
    fixed_url = 'https://i.gyazo.com/' + gyazo_id + '.png'
    if check_url(fixed_url):
        # print('png okay')
        return fixed_url
    elif check_url(fixed_url[:-3] + 'jpg'):
        fixed_url = fixed_url[:-3] + 'jpg'
        # print('jpg okay')
        return fixed_url
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
    reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')

    regex = '(?<!\w\.)gyazo\.com/\w{32}'

    reply_template_header = ('Hi, I\'m a bot that links Gyazo images directly.\n\n')
    reply_template_footer = ('^^[Source](https://github.com/Ptomerty/GyazoBot) ^^| '
                             '^^[Why?](https://github.com/Ptomerty/GyazoBot/blob/master/README.md) ^^| '
                             '^^[Creator](https://np.reddit.com/u/derpherp128) ^^| '
                             '^^[leavemealone](https://np.reddit.com/message/compose/?to=Gyazo_Bot'
                             '&subject=ignoreme&message=ignoreme)')
    global ignore
    comments = []

    refreshIgnore()

    if os.path.isfile("./comments"):
        with open("./comments", "r") as f:
            for line in f:
                comments.append(line.split("\n")[0])

    for comment in reddit.subreddit('all').stream.comments():
        refreshIgnore()
        if comment.author not in ignore and comment.id not in comments:
            list = re.findall(regex, comment.body)
            if list:
                a = reply_template_header
                for url in list:
                    fixed = process(url)
                    if (fixed != '' and fixed != None):
                        a += process(url) + '\n\n'
                if a != reply_template_header:  # make sure there's an actual fixed link
                    a += reply_template_footer
                    comment.reply(a)
                    comments.append(comment.id)
                    with open("./comments", "a+") as cmtfs:
                        cmtfs.write('{0}\n'.format(comment.id))
                        cmtfs.flush()
                        os.fsync(cmtfs.fileno())


if __name__ == '__main__':
    main()
