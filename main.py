from datetime import datetime, timedelta
import logging
import sys
import os
import requests
import json
from tweepy import Client, Forbidden
from keys import twitter_credentials

LOGGING_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

# Configure the logging to use AWS Lambda's logging handler
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# LAX is good for testing
LOCATIONS = [
    ('BNA', 10260),
    # ('MEM', 13621),
    # ('LAX', 5180)
]

DELTA = 12   # Weeks

SCHEDULER_API_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/locations/{location}/slots?startTimestamp={start}&endTimestamp={end}'
TTP_TIME_FORMAT = '%Y-%m-%dT%H:%M'

NOTIF_MESSAGE = 'New appointment slot open at {location}: {date}'
MESSAGE_TIME_FORMAT = '%A, %B %d, %Y at %I:%M %p'

def tweet(message):
    logging.info('Trying Tweet')
    try:
        t.create_tweet(text=message)
    except Forbidden as e:
        logging.error(str(e))
        if "duplicate content" in str(e):
            logging.error("This tweet was not posted because it contains duplicate content.")
        else:
            logging.error("You do not have permission to perform this action.")

def check_for_openings(location_name, location_code):
    start = datetime.now()
    end = start + timedelta(weeks=DELTA)

    url = SCHEDULER_API_URL.format(location=location_code,
                                   start=start.strftime(TTP_TIME_FORMAT),
                                   end=end.strftime(TTP_TIME_FORMAT))
    try:
        results = requests.get(url).json()  # List of flat appointment objects
    except requests.ConnectionError:
        logging.exception('Could not connect to scheduler API')
        sys.exit(1)

    for result in results:
        if result['active'] > 0:
            logging.info('Opening found for {}'.format(location_name))

            timestamp = datetime.strptime(result['timestamp'], TTP_TIME_FORMAT)
            message = NOTIF_MESSAGE.format(location=location_name,
                                           date=timestamp.strftime(MESSAGE_TIME_FORMAT))
            logging.info('Tweeting: ' + message)
            tweet(message)
            return  # Halt on first match

    logging.info('No openings for {}'.format(location_name))


def main():
    logging.basicConfig(format=LOGGING_FORMAT,
                            level=logging.INFO,
                            stream=sys.stdout)

    logging.info('Starting checks (locations: {})'.format(len(LOCATIONS)))
    for location_name, location_code in LOCATIONS:
        check_for_openings(location_name, location_code)

def lambda_handler(event, context):
    logging.info('Lambda Handler Started')
    twitter_credentials = json.loads(os.environ.get("TWTR"))
    main()

if __name__ == "__main__":
    t = Client(**twitter_credentials)    
    tweet("Test!")
    main()
