VPC Peering
===================================

**Context:**
 VPc peering understnading and usages.



What is VPC Peering:
-------------------------
A VPC peering connection is a networking connection between two VPCs that enables you to route traffic between them using private IPv4 addresses or IPv6 addresses. Instances in either VPC can communicate with each other as if they are within the same network. You can create a VPC peering connection between your own VPCs, or with a VPC in another AWS account. The VPCs can be in different regions (also known as an inter-region VPC peering connection).

What functionality is provided:
-------------------------------
-  A VPC peering connection helps you to facilitate the transfer of data. For example, if you have more than one AWS account, you can peer the VPCs across those accounts to create a file sharing network. You can also use a VPC peering connection to allow other VPCs to access resources you have in one of your VPCs. 


How is VPC Peering used:
--------------------------
- Python SDK, AWS CLI, Management Console


**Walk-thru** of setting up VPC Peering:
-------------------------------------------

- Setting up peering of VPC01 to VPC02
::

 (python36) [da@scrap ~]$  aws ec2 create-vpc-peering-connection --vpc-id vpc-0fdf62bxxx6 --peer-vpc-id vpc-0e49exxxxx44 --peer-owner-id 1234567892890
 {
     "VpcPeeringConnection": {
         "AccepterVpcInfo": {
             "OwnerId": "12345678990",
            "VpcId": "vpc-0e49e4xxxxxxx0d7",
            "Region": "us-west-2"
        },
        "ExpirationTime": "2019-02-22T16:44:16.000Z",
        "RequesterVpcInfo": {
            "CidrBlock": "192.100.1.0/24",
            "CidrBlockSet": [
                {
                    "CidrBlock": "192.100.1.0/24"
                }
            ],
            "OwnerId": "21xxxxxxxx60",
            "PeeringOptions": {
                "AllowDnsResolutionFromRemoteVpc": false,
                "AllowEgressFromLocalClassicLinkToRemoteVpc": false,
                "AllowEgressFromLocalVpcToRemoteClassicLink": false
            },
            "VpcId": "vpc-0fdf62b6xxxxxxxx8d",
            "Region": "us-west-2"
        },
        "Status": {
            "Code": "initiating-request",
            "Message": "Initiating Request to 123456789890"
        },
        "Tags": [],
        "VpcPeeringConnectionId": "pcx-0dexxxxxxxxxx9"
    }
 }


- accept peering connection from target account:
::

 aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "pcx-0de31dxxxxx2b549"

	
- update route on peer 
::


 While in the account that has VPC2:
 (python36) [da@scrap ~]$  aws ec2 create-route --route-table-id rtb-06c13dxxxxxxxx2b --destination-cidr-block 192.100.1.0/24 --vpc-peering-connection-id "pcx-0de31xxxxxxxx49"
 {
    "Return": true
 }


- Note: this must be ran on the target account that requires the route. Additionally, if you intend to create a full round about  communication where VPC1 can talk to VPC2 and vice-versa. You must update the route on both source and target 

- So to setup VPC2 to be able to communicate back we do:
::


 (python36) [da@scrap ~]$  aws ec2 create-route --route-table-id rtblkjh876y897xxxx5yb --destination-cidr-block 10.10.4.0/24 --vpc-peering-connection-id "pcx-0de31xxxxxxxx49"
  {
    "Return": true
 }

Updating Security Groups
------------------------


- ingress security group
::

 (python36) [da@scrap ~]$ aws ec2 authorize-security-group-ingress --group-id sg-0fd4f560815013a9f --protocol tcp  --source-group sg-0f59087a6a82ac871
 (python36) [da@scrap ~]$ aws-whoami
 {
    "UserId": "AROAJ2PFDMOSE2JEGS7AY:da@ait-poc-OrgAdmin",
    "Account": "217985836260",
    "Arn": "arn:aws:sts::217985836260:assumed-role/OrgAdmin/da@ait-poc-OrgAdmin"



 (python36) [da@scrap ~]$  aws ec2 authorize-security-group-ingress --group-id sg-0f59087a6a82ac871 --protocol tcp  --source-group sg-0fd4f560815013a9f
 (python36) [da@scrap ~]$ aws-whoami
 {
    "UserId": "AROAJU3BMOJ5H7RDO6GIM:da@ait-training-OrgAdmin",
    "Account": "071826132890",
    "Arn": "arn:aws:sts::071826132890:assumed-role/OrgAdmin/da@ait-training-OrgAdmin"
 }
 (python36) [da@scrap ~]$


 (python36) [da@scrap ~]$ aws-whoami
 {
    "UserId": "AROAJU3BMOJ5H7RDO6GIM:da@ait-training-OrgAdmin",
    "Account": "071826132890",
    "Arn": "arn:aws:sts::071826132890:assumed-role/OrgAdmin/da@ait-training-OrgAdmin"
 } 


 (python36) [da@scrap ~]$ aws ec2 describe-security-group-references --group-id sg-0f59087a6a82ac871
 {
    "SecurityGroupReferenceSet": [
        {
            "GroupId": "sg-0f59087a6a82ac871",
            "ReferencingVpcId": "vpc-0fdf62b63d46e078d",
            "VpcPeeringConnectionId": "pcx-0de31d992fae2b549"
        }
    ]

 (python36) [da@scrap ~]$ aws-assume-role ait-poc-OrgAdmin                                                        (python36) [da@scrap ~]$ aws ec2 describe-security-group-references --group-id sg-0fd4f560815013a9f
 {
    "SecurityGroupReferenceSet": [
        {
            "GroupId": "sg-0fd4f560815013a9f",
            "ReferencingVpcId": "vpc-0e49e447c5f0f20d7",
            "VpcPeeringConnectionId": "pcx-0de31d992fae2b549"
        }
    ]
 }




- update egress security group
::


 (python36) [da@scrap ~]$ aws ec2 authorize-security-group-egress --group-id sg-0fd4f560815013a9f  --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,,UserIdGroupPairs=[{GroupId=sg-0f59087a6a82ac871}]
 (python36) [da@scrap ~]$ aws-whoami
 {
    "UserId": "AROAJ2PFDMOSE2JEGS7AY:da@ait-poc-OrgAdmin",
    "Account": "217985836260",
    "Arn": "arn:aws:sts::217985836260:assumed-role/OrgAdmin/da@ait-poc-OrgAdmin"
 }
 (python36) [da@scrap ~]$ aws-assume-role ait-training-OrgAdmin                                                   (python36) [da@scrap ~]$ aws ec2 authorize-security-group-egress --group-id sg-0f59087a6a82ac871  --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,,UserIdGroupPairs=[{GroupId=sg-0fd4f560815013a9f}]
 (python36) [da@scrap ~]$ aws-whoami
 {
    "UserId": "AROAJU3BMOJ5H7RDO6GIM:da@ait-training-OrgAdmin",
    "Account": "071826132890",
    "Arn": "arn:aws:sts::071826132890:assumed-role/OrgAdmin/da@ait-training-OrgAdmin"
 }



Overview of results:
---------------------

- Example: pulling a file from AWS account ait-training, while logged into a server on the AWS account ait-poc utilizing the private IP space
- We must first ssh into the public address of the server in the ait-poc account as there is no VPN setup.
- once we have logged into that server, we will get the file from the server in the ait-training account via the private IP of the server in the ait-training account. (account: ait-training     Server: 10.0.0.153)  
- The private IP space for the server in ait-poc is: 192.100.1.191
::


   da-default.pem  8  kms-key-test-key
 [da@scrap keys]$ ssh ait@5x.xxx.xx0.231
 ait@5x.xxx.xxx.231's password:
 Last login: Mon Feb 25 21:54:52 2019 from scrap.com

       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

 https://aws.amazon.com/amazon-linux-2/
 9 package(s) needed for security, out of 17 available
 Run "sudo yum update" to apply all updates.
 [ait@ip-192-100-1-191 ~]$ ls

 [ait@ip-192-100-1-191 ~]$

 [ait@ip-192-100-1-191 ~]$ scp ait@10.0.0.153:~/test_file .
 ait@10.0.0.153's password:
 test_file                                                                                                  100%   38    30.5KB/s   00:00
 [ait@ip-192-100-1-191 ~]$ ls
 test_file
 [ait@ip-192-100-1-191 ~]$

