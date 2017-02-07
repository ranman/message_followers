import time
import cfnresponse
import os

import boto3

import twitter

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('DDB_TABLE'))

api = twitter.Api(
    os.getenv('CONSUMER_KEY'),
    os.getenv('CONSUMER_SECRET'),
    os.getenv('ACCESS_TOKEN_KEY'),
    os.getenv('ACCESS_TOKEN_SECRET'),
)


def lambda_handler(event, context):
    try:
        if event['RequestType'] in ['Delete', 'Update']:
            cfnresponse.send(event, context, cfnresponse.SUCCESS)
            return
        timestamp = int(time.time())
        num_followers = 0
        with table.batch_writer() as batch:
            for follower in api.GetFollowerIDs():
                num_followers += 1
                batch.put_item(
                    Item={'follower': follower, 'timestamp': timestamp}
                )
        resp_data = {'followers_loaded': num_followers, 'elapsed': int(time.time()) - timestamp}
        cfnresponse.send(event, context, cfnresponse.SUCCESS, resp_data)
    except Exception as ex:
        print ex
        cfnresponse.send(event, context, cfnresponse.FAILED, {'error': str(ex)})
