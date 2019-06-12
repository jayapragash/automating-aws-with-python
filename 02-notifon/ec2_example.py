# coding: utf-8
import boto3
session = boto3.Session(profile_name='JPNEW')
ec2 = session.resource('ec2')
keyname = newkey
keypath = keyname + '.pem'
key = ec2.create_key_pair(KeyName=keyname)
with open(keypath , 'w') as keyfile:
    keyfile.write(key.key_material)
image =ec2.Image('ami-04768381bf606e2b3')
instance = ec2.create_instances(ImageId=image.id, MinCount= 1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
inst = instance[0]
inst.reload()
inst.public_dns_name

as_client = session.client('autoscaling')
as_client.describe_auto_scaling_groups()
as_client.describe_policies()
as_client.execute_policy(AutoScalingGroupName='slack-notify', PolicyName='simple scale up')
as_client.execute_policy(AutoScalingGroupName='slack-notify', PolicyName='simple scale down')
