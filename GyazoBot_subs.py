import praw
import requests
import os

ignore = []

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
    if os.path.isfile("./ignore"):
        with open("./ignore", "r") as f:
            for line in f:
                ignore.append(line.split("\n")[0])

def main():
    reply_template = ('Hi, I\'m a bot that links Gyazo images directly.'
                      '\n\n{}\n\n'
                      '^^[Source](https://github.com/Ptomerty/GyazoBot) ^^| '
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

    reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')
    for submission in reddit.subreddit('all').stream.submissions():
        refreshIgnore()
        if not submission.author in ignore and not submission.id in posts:
            fixed = process(submission)
            if fixed is not '' and fixed is not None:
                reply_text = reply_template.format(process(submission))
                submission.reply(reply_text)
                posts.append(submission.id)
                with open("./posts", "a+") as postfs:
                    postfs.write('{0}\n'.format(submission.id))
                    postfs.flush()
                    os.fsync(postfs.fileno())


if __name__ == '__main__':
    main()
