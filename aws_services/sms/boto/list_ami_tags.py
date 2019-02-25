#!/usr/bin/env python
import sys
import re
import boto3
from organizer.utils import yamlfmt

# get AMI id
if len(sys.argv) > 1:
    ami_id = sys.argv[1]
else:
    ami_id = None


ec2_client = boto3.client('ec2')
if ami_id:
    response = ec2_client.describe_tags(
        Filters=[dict(
            Name='resource-id',
            Values=[ami_id],
        )],
    )
    print(yamlfmt(response['Tags']))
