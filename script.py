import asyncio
import os
from datetime import datetime, timedelta, timezone
from twikit import Client

client = Client('en-US')

auth_token = os.getenv('AUTH_TOKEN')
ct0 = os.getenv('CT0')
screen_name = os.getenv('SCREEN_NAME')

client.set_cookies({
    "auth_token": auth_token,
    "ct0": ct0
})

async def delete_old_tweets():
    now = datetime.now(timezone.utc)
    user = await client.get_user_by_screen_name(screen_name)
    tweets = await user.get_tweets('Tweets', count=20)
    
    while tweets:
        for tweet in tweets:
            tweet_created_at = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
            tweet_age = now - tweet_created_at
            if tweet_age > timedelta(hours=24):
                await client.delete_tweet(tweet.id)
                masked_id = tweet.id[:-10] + '**********'
                print(f"Deleted tweet ID: {masked_id}")

        tweets = await tweets.next() if tweets else None
        if not tweets:
            print("No more tweets found. Stopping.")
            break

async def main():
    await delete_old_tweets()

asyncio.run(main())
