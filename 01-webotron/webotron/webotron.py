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

import boto3
from botocore.exceptions import ClientError
import click
from domain import DomainManager
import util
from bucket import BucketManager

session = None
bucket_manager = None
domain_manager = None


@click.group()
@click.option('--profile', default = None, help="Use a given AWS profile")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager, domain_manager
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)


@cli.command('list-buckets')
def list_buckets():
    """List all buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List Objects in an s3 Bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure s3 Bucket."""
    s3bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3bucket)
    bucket_manager.configure_website(s3bucket)
    return


@cli.command('sync')
@click.argument("pathname", type=click.Path(exists=True))
@click.argument("bucket")
def sync(pathname, bucket):
    """Sync contents of PATHNAME to s3 Bucket."""
    bucket_manager.sync(pathname,bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure DOMAIN to point to BUCKET."""
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)

    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    domain_manager.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configure: http://{}".format(domain))


if __name__ == '__main__':
    cli()
