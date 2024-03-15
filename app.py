import os
import time
from dotenv import load_dotenv
from twikit import Client
from twikit.utils import build_query
from datetime import datetime, timezone, timedelta

# Load environment variables from .env file
load_dotenv()


#### Authentication START ####

# Credentials of the twitter account used to scrape tweets (Due to the recent twitter scraping policy changes, every account has a limit of viewing tweets i,e scraping tweets)
# Access environment variables
USERNAME = os.environ.get('TWITTER_USERNAME')
EMAIL = os.environ.get('TWITTER_EMAIL')
PASSWORD = os.environ.get('TWITTER_PASSWORD')


# Initialize client
client = Client('en-US')
# Login to the service with provided user credentials
client._user_agent = client._user_agent.strip()

client.login(
    auth_info_1=USERNAME,
    auth_info_2=EMAIL,
    password=PASSWORD
)

#### Authentication END ####


def stock_scrapper(twitter_accounts_list, stock_ticker, time_interval):
    while True:
        # Converting the time interval to a compatible format
        time_to_subtract = timedelta(
            days=time_interval[0], hours=time_interval[1], minutes=time_interval[2])

        # Subtract the timedelta from the datetime
        targeted_datetime = datetime.now(timezone.utc) - time_to_subtract

        # Converting the targeted datetime to a compatible formate for the options dictionary "since" value
        formatted_date = targeted_datetime.strftime("%Y-%m-%d")

        # counter of the tweets mentioning the ticker
        counter_of_qualified_tweets = 0

        # Targeted stock ticker
        text = stock_ticker

        # Iterate over the list of targeted twitter accounts
        for user_name in twitter_accounts_list:

            options = {
                # The name of the account to be scraped
                "from_user": user_name,
                "exact_phrases": None,
                "or_keywords": None,
                "exclude_keywords": None,
                "hashtags": None,
                "to_user": None,
                "mentioned_users": None,
                "filters": None,
                "exclude_filters": None,
                "urls": None,
                # Setting a cutoff date for optimize scraping and less consumption of reading rates
                "since": formatted_date,
                "until": None,
                "positive": None,
                "negative": None,
                "question": None
            }
            query = build_query(text, options)

            # Search latest tweets using the query generated
            tweets = client.search_tweet(query, 'latest')

            for tweet in tweets:
                # Convert the tweet datetime to a compatible datetime
                tweet_datetime = datetime.strptime(
                    tweet.created_at, "%a %b %d %H:%M:%S %z %Y")
                # If the tweet was tweeted in the targeted datetime range
                if targeted_datetime <= tweet_datetime:
                    counter_of_qualified_tweets += 1
                    # printing the tweet id for testing purposes
                    print(tweet, user_name, tweet.created_at)

        print(stock_ticker + " was mentioned " + str(counter_of_qualified_tweets) + " times in the last " +
              str(time_interval[0]) + " days, " + str(time_interval[1]) + " hours, and " + str(time_interval[2]) + " minutes.")
        print("######################################################################")

        # Calculate the time interval in seconds
        time_interval_in_seconds = (
            time_interval[0] * 24 * 60 * 60) + (time_interval[1] * 60 * 60) + (time_interval[2] * 60)
        # Sleep for the time interval
        time.sleep(time_interval_in_seconds)


stock_scrapper(["Mr_Derivatives", "warrior_0719",
               "ChartingProdigy", "allstarcharts", "yuriymatso", "TriggerTrades", "AdamMancini4", "CordovaTrades", "Barchart", "RoyLMattox"], "$spx", [1, 12, 0])
