import tweepy
import sys
import settings as s
import matplotlib.pyplot as plt
from pandas import DataFrame

# twitter authentication
auth = tweepy.OAuthHandler(s.API_KEY, s.API_SECRET)
auth.set_access_token(s.ACCESS_TOKEN, s.ACCESS_SECRET)

# create an API object 
# from this API object, we can access several methods in the twitter API
api = tweepy.API(auth, wait_on_rate_limit=True)

timeline = api.home_timeline()

# retrieve my own tweets
def retrieve_my_tweets():
    tweets = api.user_timeline (screen_name=s.MY_USER_ID, count=200, include_rts=False, tweet_mode='extended')
    for info in tweets[:3]:
        print("ID: {}".format(info.id))
        print(info.full_text)
        print("\n")

# tweet something, anything
def tweet_from_bot(twt):
    try:
        msg = "[{}]: {} ".format(s.MY_HANDLE_NAME, twt)
        api.update_status(msg)
        print("[{}] tweet succesfully posted: {}".format(s.MY_HANDLE_NAME, twt))
        # after posting a tweet, get my last three tweets and show it on terminal
        retrieve_my_tweets()
    except Exception as e:
        print("exception encountered in tweet_from_bot")
        print(e)

# reply to a tweet given a tweet ID
def reply_to_tweet(twt, twt_id):
    try:
        msg = "[{}]: {} ".format(s.MY_HANDLE_NAME, twt)
        api.update_status(status=msg, in_reply_to_status_id=twt_id)
        print("[{}] tweet succesfully posted: {}".format(s.MY_HANDLE_NAME, twt))
        # after posting a tweet, get my last three tweets and show it on terminal
        retrieve_my_tweets()
    except Exception as e:
        print("exception encountered in reply_to_tweet")
        print(e)

# retrieve tweets from a user
def retrieve_tweets(user):
    tweets = api.user_timeline (screen_name=user, count=200, include_rts=False, tweet_mode='extended')
    for info in tweets[:10]:
        print("ID: {}".format(info.id))
        print(info.full_text)
        print("\n")

# retrieve tweets and save to a csv file
def save_tweets_to_csv(user):
    tweets = api.user_timeline (screen_name=user, count=200, include_rts=False, tweet_mode='extended')
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    # loop through the user's timeline
    while True:
        tweets = api.user_timeline (screen_name=user, count=200, include_rts=False, max_id=oldest_id-1, tweet_mode='extended')
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print('{} tweets downloaded'.format(len(all_tweets)))
    # since we have populated the all_tweets array, 
    # then we can output the tweets into a csv
    print('Creating %s_tweets.csv --' % user)
    for tweet in all_tweets:
        outtweets = [[tweet.id_str,
                    tweet.created_at,
                    tweet.favorite_count,
                    tweet.retweet_count,
                    tweet.full_text.encode("utf-8").decode("utf-8")] 
                    for idx, tweet in enumerate(all_tweets)]
        df = DataFrame(outtweets, columns=["id","created_at","favorite_count","retweet_count","text"])
        df.to_csv('%s_tweets.csv' % user, index=False)
        df.head(3)
        print('Tweet ID %s successfully inserted into csv' % tweet.id_str)

# retrieve tweets and generate preliminary analysis
def generate_prelim_analysis(user):
    tweets = api.user_timeline (screen_name=user, count=200, include_rts=False, tweet_mode='extended')
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    # loop through the user's timeline
    while True:
        tweets = api.user_timeline (screen_name=user, count=200, include_rts=False, max_id=oldest_id-1, tweet_mode='extended')
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print('{} tweets downloaded'.format(len(all_tweets)))
    # since we have populated the all_tweets array, 
    # then we can output the tweets into a csv
    print('Generating preliminary analysis for %s --' % user)
    for tweet in all_tweets:
        outtweets = [[tweet.id_str,
                    tweet.created_at,
                    tweet.favorite_count,
                    tweet.retweet_count,
                    tweet.full_text.encode("utf-8").decode("utf-8")] 
                    for idx, tweet in enumerate(all_tweets)]
        df = DataFrame(outtweets, columns=["id","created_at","favorite_count","retweet_count","text"])
        ylabels = ["favorite_count", "retweet_count"]
        fig = plt.figure(figsize=(13,3))
        fig.subplots_adjust(hspace=4,wspace=0.01)

        n_row = len(ylabels)
        n_col = 1
        for count, ylabel in enumerate(ylabels):
            ax = fig.add_subplot(n_row,n_col,count+1)
            ax.plot(df["created_at"],df[ylabel])
            ax.set_ylabel(ylabel)
        plt.show()

# make global fns callable from terminal
if __name__ == '__main__':
    args = sys.argv
    globals()[args[1]](*args[2:])
