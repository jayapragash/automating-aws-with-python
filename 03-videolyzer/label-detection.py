# coding: utf-8
import boto3
session = boto3.Session(profile_name='JPNEW')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='jpvideolyzerbucket' , CreateBucketConfiguration={'LocationConstraint':session.region_name})
from pathlib import Path
bucket.upload_file(r'C:\Users\JP\Downloads\Pexels.mp4' , 'Pexels')
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(Video= {'S3Object':{'Bucket':'jpvideolyzerbucket', 'Name':'Pexels'}})
response
result = rekognition_client.get_label_detection(JobId='36d923b77521d9e31507752f54f2ecc81e9a5c4b93299bab5a9afd809d0918bd')
result
result.keys()
result['JobStatus']
result['VideoMetadata']
result['ResponseoMetadata']
result['Labels']
