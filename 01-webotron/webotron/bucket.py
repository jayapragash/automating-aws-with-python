# -*- coding: utf-8 -*-
"""Classes for s3 Buckets."""

from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError
import util

class BucketManager:
    """Manage an S3 Bucket."""

    def __init__(self, session):
        """Create a Bucket Manager Object."""
        self.session = session
        self.s3 = self.session.resource('s3')

    def get_region_name(self, bucket):
        """Get the bucket's region name."""
        client = self.s3.meta.client
        bucket_location = client.get_bucket_location(Bucket=bucket.name)

        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Get the website URL for this bucket."""
        return "http://{}.{}".format(
            bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host
            )


    def all_buckets(self):
        """Get an iterator for all the buckets."""
        return self.s3.buckets.all()


    def all_objects(self,bucket):
        """Get an iterator for all objects in bucket."""
        return self.s3.Bucket(bucket).objects.all()


    def init_bucket(self,bucket_name):
        """Create an Bucket for uploading contents or return existing One"""
        s3bucket = None
        try:
            s3bucket = self.s3.create_bucket(Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint' : self.session.region_name})
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3bucket = self.s3.Bucket(bucket_name)
            else:
                raise error
        return s3bucket


    def set_policy(self, bucket):
        """set bucket policy to be readable by everyone."""
        policy = """
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::%s/*"
                    ]
                }
            ]
        }"""%bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy=policy)


    def configure_website(self,bucket):
        """This will configure the website."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })


    @staticmethod
    def upload_file(bucket, path, key):
        """Upload Path to S3_Bucket at key."""
        content_type = mimetypes.guess_type(key)[0] or "text/plain"
        bucket.upload_file(path, key, ExtraArgs={'ContentType':content_type})


    def sync(self, pathname, bucket_name):
        """Sync the contents of the Filepath and s3 Buckets"""
        bucket = self.s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()
        def handler_directory(target):
            for path in target.iterdir():
                if path.is_dir(): handler_directory(path)
                if path.is_file(): self.upload_file(bucket,str(path), str(path.relative_to(root)).replace("\\","/"))
        handler_directory(root)
