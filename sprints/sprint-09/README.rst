AIT Sprint 9
============

Learning POC for AWS Transit Gateway


Private Data in Codecommit
--------------------------

account
  ait-poc

repository
  https://git-codecommit.us-west-2.amazonaws.com/v1/repos/sprint9_data


Goals
-----

- develop understaning of AWS network technologies:

  - VPC Peering
  - Transit Gateway
  - Transit VPC
  - AWS Resource Mananer

- build multiple accounts/VPCs for prototype

  - AWS CDK

- build and demonstrate functioning prototype network environment

  - network hub with TGW
  - site-to-site VPN to on-prem datacenter

- develop test cases to validate networking - see `Private Data in Codecommit`_

  - tgw_testing.rst

- demonstrate trouble shooting techniques

  - VPC flowlogs
  - Cloudwatch Dashboard for TGW   
  - EC2 instance tools

    - tcpdump
    - traceroute


What's Next
-----------

- network traffic visualization

  - query combined vpc flowlogs using S3/Athena

- integrate Direct Connect into Network Hub

  - DX with TGW not yet supported
