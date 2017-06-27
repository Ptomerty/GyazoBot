import praw
import os
import praw.models

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
    try:
        for item in reddit.inbox.stream():
            if isinstance(item, praw.models.Message):
                checkMsg(item)
                item.mark_read()
    except:
        # misc timeout
        time.sleep(45)  # "timed out error"
        print("timeout error?");


if __name__ == '__main__':
    main()
