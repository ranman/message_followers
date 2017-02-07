from base64 import b64decode
import os
import time

import boto3

import twitter

dynamodb = boto3.resource('dynamodb')
kms = boto3.client('kms')
table = os.getenv('DDB_TABLE')


def decrypt(var):
    """Helper function to decrypt our environment variables"""
    return kms.decrypt(CipherTextBlob=b64decode(var))['Plaintext']

# TODO: enable KMS encryption/decryption

api = twitter.Api(
    os.getenv('CONSUMER_KEY'),
    os.getenv('CONSUMER_SECRET'),
    os.getenv('ACCESS_TOKEN_KEY'),
    os.getenv('ACCESS_TOKEN_SECRET')
)

direct_message = os.getenv('MESSAGE')


def lambda_handler(event, context):
    followers = set(api.GetFollowerIDs())
    ddb_followers = table.scan(ProjectionExpression="follower")["Items"]
    old_followers = set([int(x['follower']) for x in ddb_followers])
    timestamp = int(time.time())

    new_followers = followers - old_followers
    for new_follower in new_followers:
        table.put_item(Item={'follower': new_follower, 'timestamp': timestamp})
        api.PostDirectMessage(direct_message, user_id=new_follower)
