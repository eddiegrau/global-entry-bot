# Global Entry Appointment Bot

A Twitter bot that announces open Global Entry interview slots.

Forked from [guoguo12/global-entry-bot](https://github.com/guoguo12/global-entry-bot)

Based largely on [oliversong/goes-notifier](https://github.com/oliversong/goes-notifier),
[mvexel/next_global_entry](https://github.com/mvexel/next_global_entry),
and [this comment](https://github.com/oliversong/goes-notifier/issues/5#issuecomment-336966190).

This project is (obviously) not affiliated with U.S. Customs and Border Protection or any airport.

## Installation

Install dependencies with

```
pip install -r requirements.txt
```

Then put your Twitter API credentials in a file called `keys.py`, which should define `twitter_credentials`:

```python
twitter_credentials = dict(consumer_key='',
                           consumer_secret='',
                           access_token_key='',
                           access_token_secret='')
```

This repo is setup to auto deploy to Lambda and will run every 10 minutes. 
My version is live [here](https://twitter.com/Marvs_GE_Bot)
