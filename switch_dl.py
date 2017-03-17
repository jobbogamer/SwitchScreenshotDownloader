
import twitter
import os
import sys
import argparse
import urllib2
import shutil
from datetime import datetime


def get_api():
    """
    Get the API keys from environment variables and create a Twitter API instance.
    These variables are:
    - SSDL_CONSUMER_KEY
    - SSDL_CONSUMER_SECRET
    - SSDL_ACCESS_TOKEN_KEY
    - SSDL_ACCESS_TOKEN_SECRET
    """
    keys = {
        'consumer_key':        os.getenv('SSDL_CONSUMER_KEY', None),
        'consumer_secret':     os.getenv('SSDL_CONSUMER_SECRET', None),
        'access_token_key':    os.getenv('SSDL_ACCESS_TOKEN_KEY', None),
        'access_token_secret': os.getenv('SSDL_ACCESS_TOKEN_SECRET', None)
    }

    # If any of the environment variables couldn't be found, give up here.
    for item in keys:
        if keys[item] is None:
            print 'Missing environment variable: {}'.format(item)
            sys.exit(1)

    return twitter.Api(**keys)


def get_tweets(username):
    """
    Get a certain number of the latest tweets from a given user.
    """
    api = get_api()
    return api.GetUserTimeline(screen_name=username)


def save_photo(url, target_path):
    """
    Get the photo at the given URL and save it to the given path.
    """
    img = urllib2.urlopen(url)
    with open(target_path, 'w') as f:
        f.write(img.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--latest', action='store_true')
    parser.add_argument('-n', '--number', type=int, default=1)
    parser.add_argument('-t', '--require_tag', type=str)
    parser.add_argument('username', type=str)
    parser.add_argument('output_dir', type=str)
    args = parser.parse_args()

    # Add trailing slash to output_dir if necessary.
    if not args.output_dir.endswith('/'):
        output_dir = args.output_dir + '/'
    else:
        output_dir = args.output_dir

    # Fetch the tweets.
    tweets = get_tweets(args.username)
    
    # The main event: looping over the tweets to get images. We assume that the
    # twitter API returns them in reverse chronological order (i.e. newest tweet
    # first) so that we can start at the start of the list.
    found_images = 0
    for tweet in tweets:
        if tweet.media is not None and len(tweet.media) > 0:
            for media in tweet.media:
                if media.type == 'photo':
                    # Always use the "large" size because for a Switch screenshot it'll be the
                    # full 1280x720 image.
                    large_url = media.media_url + ':large'

                    sub_dir = ''
                    if tweet.hashtags is not None and len(tweet.hashtags) > 0:
                        # To save effort when posting tweets from the Switch, ignore
                        # the default #NintendoSwitch hashtag.
                        hashtags = [tag.text.lower() for tag in tweet.hashtags if tag.text != 'NintendoSwitch']

                        # If --require_tag was passed, check that the tag was given.
                        if args.require_tag is not None:
                            if args.require_tag.lower() not in hashtags:
                                continue

                        # Add each hashtag in turn, i.e. a tweet with
                        # "#BreathoftheWild #Shrine #TestOfStrength"
                        # would be downloaded to {output_dir}/breathofthewild/shrine/testofstrength.
                        for tag in hashtags:
                            sub_dir += tag + '/'

                    elif args.require_tag is not None:
                        # The tweet has no hashtags and --require_tag was passed.
                        continue

                    # Attempt to create the target directory, ignoring any errors
                    # because they probably mean the directory already exists.
                    target_dir = output_dir + sub_dir
                    try:
                        os.makedirs(target_dir)
                    except:
                        pass

                    # Contort the tweet's date into a filename. (Going to unix timestamps first
                    # is easier because tweet.created_at is actually a string.)
                    unix_date = tweet.created_at_in_seconds
                    date = datetime.fromtimestamp(unix_date)
                    str_date = date.strftime('%Y-%m-%d at %H-%M-%S')
                    filename = str_date + '.jpg'

                    # Build entire target file path and download the photo.
                    target_path = target_dir + filename
                    save_photo(large_url, target_path)
                    print 'Downloaded {}'.format(filename)

                    # If requested, make a copy of the image at the top level of the output dir
                    # called latest.jpg. This should only be done for the first image we process
                    # since the tweets are in reverse chronological order.
                    if args.latest and found_images == 1:
                        latest_path = output_dir + 'latest.jpg'
                        shutil.copyfile(target_path, latest_path)

                    # Stop when we have downloaded the requested number.
                    found_images += 1
                    if found_images == args.number:
                        sys.exit(0)

