import slack
import random
import os
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

load_dotenv()
app = Flask(__name__)

'''
Required Slack API Secret and Bot token - please update .env-sample with your
OAuth token and client secret, then rename to .env
'''
slack_event_adapter = SlackEventAdapter(
    os.environ['SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']


# Responses for "Fuck you Shoresy"
with open("quotes/quotes.txt") as file:
    quotes = file.read()
    quote = list(map(str, quotes.split("\n")))

# Responses to "What's going to happen?"
with open("quotes/fight.txt") as file:
    fights = file.read()
    fight = list(map(str, fights.split("\n")))

'''
Variations of trigger phrases
'''
fight_words = ["what's gunna happen", "whats gunna happen", "what's gonna happen",
               "whats gonna happen", "what's going to happen", "whats going to happen"]

shoresy = ['fuck you shoresy', 'fuck you, shoresy']


@slack_event_adapter.on('message')
def message(payload):
    '''Get payload from Slack API then pull out channel, user, and user message '''
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID == user_id:
        return

    else:

        if any(word in text.lower() for word in shoresy):
            reply_list = random.choices(quote, k=3)
            quote_reply = random.choice(reply_list)
            random_reply = quote_reply.replace("{mention}", f'<@{user_id}>')
            client.chat_postMessage(channel=channel_id, text=random_reply)

        if "fucking embarrassing" in text.lower():
            client.chat_postMessage(
                channel=channel_id, text="https://raw.githubusercontent.com/dlchamp/LetterkennyBot/main/img/embarrassing.gif")

        if any(word in text.lower() for word in fight_words):
            random_fight = random.choice(fight)
            client.chat_postMessage(channel=channel_id, text=random_fight)

        if "how are ya now" in text.lower():
            client.chat_postMessage(channel=channel_id, text="Good'n you?")

        if "to be fair" in text.lower():
            client.chat_postMessage(
                channel=channel_id, text="https://raw.githubusercontent.com/dlchamp/LetterkennyBot/main/img/to_be_fair.gif")

        if "toughest guy" in text.lower():
            client.chat_postMessage(
                channel=channel_id, text="https://raw.githubusercontent.com/dlchamp/LetterkennyBot/main/img/end_of_the_laneway.jpg")

        if "happy birthday" in text.lower():
            client.chat_postMessage(
                channel=channel_id, text='https://raw.githubusercontent.com/dlchamp/LetterkennyBot/main/img/birthday.gif')

        if "what i appreciates" in text.lower():
            client.chat_postMessage(
                channel=channel_id, text=f'Take about 10 to 15% off\'er there, <@{user_id}>')


if __name__ == '__main__':
    app.run(debug=True)
