import time
import json

import boto3
from botocore.client import Config

import twitter

s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('twitter_followers')

CREDS_BUCKET = 'ranman-application-credentials'
TWITTER_CREDS = 'message_followers.json'


def get_api_credentials(key):
    return json.loads(s3_client.get_object(
        Bucket=CREDS_BUCKET,
        Key=key
    )['Body'].read())


api = twitter.Api(**get_api_credentials(TWITTER_CREDS))

direct_message = """\
Hello! Thanks for following me!
Let me know if I can help you out with anything AWS related.
You can shoot me a message at randhunt@amazon.com or on twitter.
"""

def lambda_handler(event, context):
    followers = set(api.GetFollowerIDs())
    ddb_followers = table.scan(ProjectionExpression="follower")["Items"]
    old_followers = set([int(x['follower']) for x in ddb_followers])
    timestamp = int(time.time())

    new_followers = followers - old_followers
    for new_follower in new_followers:
        table.put_item(Item={'follower': new_follower, 'timestamp': timestamp})
        api.PostDirectMessage(direct_message, user_id=new_follower)
