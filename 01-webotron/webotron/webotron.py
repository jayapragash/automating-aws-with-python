#!/usr/bin/python
# =*- coding: utf-8 -*-

"""Webotron: Deploys websites with aws.

Webotron automates the process of deploying static websites to AWS
- Configure aws s3 buckets
 - Create them
 - set them up for static Website hosting
 - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS Cloud Front
"""

from pathlib import Path
import mimetypes
import boto3
from botocore.exceptions import ClientError
import click


session = boto3.Session(profile_name="JP")
s3 = session.resource('s3')


@click.group()
def cli():
    """Webotron deploys websites to AWS."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all buckets."""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List Objects in an s3 Bucket."""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure s3 Bucket."""
    s3bucket = None
    try:
        s3bucket = s3.create_bucket(Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint' : session.region_name})
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3bucket = s3.Bucket(bucket)
        else:
            raise error

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
    }"""%s3bucket.name
    policy = policy.strip()
    pol = s3bucket.Policy()
    pol.put(Policy=policy)
    s3bucket.Website().put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })

    return


def upload_file(s3_bucket, path, key):
    """Upload Path to S3_Bucket at key."""
    content_type = mimetypes.guess_type(key)[0] or "text/plain"
    s3_bucket.upload_file(path, key, ExtraArgs={'ContentType':content_type})


@cli.command('sync')
@click.argument("pathname", type=click.Path(exists=True))
@click.argument("bucket")
def sync(pathname, bucket):
    """Sync contents of PATHNAME to s3 Bucket."""
    root = Path(pathname).expanduser().resolve()
    s3bucket = s3.Bucket(bucket)
    def handler_directory(target):
        for path in target.iterdir():
            if path.is_dir(): handler_directory(path)
            if path.is_file(): upload_file(s3bucket,str(path), str(path.relative_to(root)).replace("\\","/"))
    handler_directory(root)


if __name__ == '__main__':
    cli()