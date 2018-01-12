import praw
import os
import praw.models
import requests.exceptions
import re

ignore = []

def checkMsg(message, reddit):
    global ignore
    regex = '(?<!\w\.)gyazo\.com/\w{32}'
    splitbody = message.body.split(' ')
    if message.body == 'ignoreme' and message.author not in ignore:
        print('ignore found')
        addToIgnore(message.author)
    elif len(splitbody) == 2 and splitbody[0] == 'delete' and splitbody[1] is not '':
        print('delete found')
        try:
            checkcomment = reddit.comment(splitbody[1])
            list = re.findall(regex, checkcomment.parent().body)
            if not list and message.author == checkcomment.parent().author and checkcomment.author == 'Gyazo_Bot':
                checkcomment.delete()
                print('fixed comment deleted!')
        except praw.exceptions.PRAWException as e:
            # invalid comment probably
            print('PRAW Exception: {}'.format(e))
            pass
        except Exception as e:
            print(e)

def addToIgnore(name):
    global ignore
    ignore.append(name)
    with open("./ignore", "a+") as f:
        f.write('{0}\n'.format(name))
        f.flush()
        os.fsync(f.fileno())

def main():
    reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')
    global ignore
    if os.path.isfile("./ignore"):
        with open("./ignore", "r") as f:
            for line in f:
                ignore.append(line.split("\n")[0])
    while True:
        try:
            for item in reddit.inbox.stream():
                if isinstance(item, praw.models.Message):
                    checkMsg(item, reddit)
                    item.mark_read()
        except requests.exceptions.ReadTimeout:
            # misc timeout
            print("timeout error")
            pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
