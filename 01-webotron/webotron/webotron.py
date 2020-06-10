#!/c/Python38/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites with aws.

Webotron automates the process of deploying statis websites
- Configure AWS S3 bucket
    - Create them
    - Set them up for statis web hosting
    - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS
"""

import boto3
import click

from bucket import BucketManager
from domain import DomainManager
import util

session = None
bucket_manager = None
domain_Manager = None


@click.group()
@click.option('--profile', default=None,
        help="Use a given AWS profile.")
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
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in a s3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync content of PATHNAME to BUCKET."""
    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure DOMAIN to point to BUCKET."""
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) \
            or domain_manager.create_hosted_zone(domain)

    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    a_record = domain_manager.create_s3_domain_record(zone, domain, endpoint)
    # for this to work the bucket name should match the domain we are deplying to
    print("Domain configure: http://{}".format(domain))

    print(a_record)


if __name__ == '__main__':
    cli()
