#  Copyright 2016 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
#  This file is licensed to you under the AWS Customer Agreement (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at http://aws.amazon.com/agreement/ .
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
#  See the License for the specific language governing permissions and limitations under the License.

from botocore.vendored import requests
import json

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send(event, context, response_status, response_data=None, resource_id=None):
    response_url = event['ResponseURL']

    print response_url

    response = json.dumps({
        'Status': response_status,
        'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': resource_id or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    })

    print "Response body:\n" + response

    # headers = {
    #     'content-type': '',
    #     'content-length': str(len(response))
    # }

    try:
        resp = requests.put(response_url, data=response)
        print "Status code: " + resp.reason
    except Exception as e:
        print "send(..) failed executing requests.put(..): " + str(e)
