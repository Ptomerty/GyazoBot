import praw
import os
import praw.models
import requests.exceptions

ignore = []

def checkMsg(message):
    global ignore
    if message.body == 'ignoreme' and message.author not in ignore:
        addToIgnore(message.author)

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
                    checkMsg(item)
                    item.mark_read()
        except requests.exceptions.ReadTimeout:
            # misc timeout
            print("timeout error")
            pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
