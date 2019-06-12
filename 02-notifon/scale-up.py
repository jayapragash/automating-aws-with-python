# coding: utf-8
import boto3
session = boto3.Session(profile_name='JPNEW')
as_client = session.client('autoscaling')
as_client.execute_policy(AutoScalingGroupName='slack-notify', PolicyName='simple scale up')
