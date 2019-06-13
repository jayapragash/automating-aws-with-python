# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-2', 'eventTime': '2019-06-12T22:44:11.746Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDAQP4XODHMPAOYO5NDN'}, 'requestParameters': {'sourceIPAddress': '174.127.175.15'}, 'responseElements': {'x-amz-request-id': '176DDDB20E7E4314', 'x-amz-id-2': 'wS6QukkD7IwUmdHSzKsTpl1KGIA/qSqirnbt+zPzQYZucCtBoaBkG8eYiZqCPcf465H5ZP6O/Kk='}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'eaf13b36-9019-47fb-ab39-10ec1191952a', 'bucket': {'name': 'jpvideolyzerbucket', 'ownerIdentity': {'principalId': 'A1NL7WF8LGJTBZ'}, 'arn': 'arn:aws:s3:::jpvideolyzerbucket'}, 'object': {'key': 'Pexels.mp4', 'size': 4581536, 'eTag': 'c894de1c0ecd044b0dfb09657934af73', 'sequencer': '005D018033F9D0299F'}}}]}
event
event[0]['s3']['name']
event[0]['s3']['bucket']['name']
event['records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['bucket']['name']
import urllib
urllib.parse.unquote_plus9event['Records'][0]['s3']['object']['key']
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
