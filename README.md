# NotifyBot

Official bot is available in Telegram as @shoutnotifbot

## What does it do?

The bot receives text from applications then sends text to you in Telegram.

## Possible use cases

Useful when you want to be instantly notified.
For example:

1.  When your app shuts down
2.  When you want feedback from your bot's users to be transfered to you
3.  When someone logins to your server
4.  
The list goes on.

## Quick example
Test it yourself in 3 easy steps

1. Talk to the bot, ask for a key using `/key`. Use `/help` to get a `link`.
2. Send a POST HTTP request. You can use any HTTP client from linux `curl` to the HTTP library in your programming language.
  Python example:
  ```
link = <your_link>
text = 'Urgent!'
import requests
requests.post(link, data={'text': text})
```
  Obviously replace `<your_link>` with the link the bot gives you.

3. You will get the "Urgent!" message from the bot.

Feel free to fork, create issues and run your copies of this simple bot.

The bot is built with  `flask`, `python-telegram-bot` and `sqlalchemy`.
