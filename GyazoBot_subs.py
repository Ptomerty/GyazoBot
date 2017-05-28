import praw

reddit = praw.Reddit('GyazoBot', user_agent='GyazoBot by derpherp128')

allsubs = reddit.subreddit('ZXhwb3NlX2tyZXNfYmFv')
reply_template = 'Hi, I\'m a bot that directly links Gyazo images.'
'\n\n{}\n\n'
'^^ ([Creator](https://reddit.com/u/derpherp128)'

for submission in allsubs.stream.submissions():
    url = submission.url
    if "gyazo.com" in url and "i.gyazo.com" not in url:
        split_arr = url.split("/")
        print(split_arr)
        if len(split_arr) >= 4:
            gyazo_id = split_arr[3] #it's an actual gyazo image
            print(submission.url)
            fixed_url = 'https://i.gyazo.com/' + gyazo_id + '.png'
            reply_text = reply_template.format(fixed_url)
            submission.reply(reply_text)