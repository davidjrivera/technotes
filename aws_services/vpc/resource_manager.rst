Amazon Resource Access Manager
==============================

what is it?

AWS Resource Access Manager (RAM) is a service that enables you to easily and securely share AWS resources with any AWS account or within your AWS Organization. You can share AWS Transit Gateways, Subnets, AWS License Manager configurations, and Amazon Route 53 Resolver rules resources with RAM.

How do you do it?

You can use an amazon SDK, AWS cLI or management Console. You create a resource share, name it, give it access to other accounts. When you share a resource with another account, then that account is granted access to the resource. Any policies and permissions in that account apply to the shared resource.


Share resources that you own, create a resource share, add the resources to share, and specify the principals with whom they are to be shared that Can be shared?

- Amazon Route 53 resolver

- Transit Gateway 

- subnets

- Configuring License Manager


We are currently using it for Transit Gateway as a way to give the targets account access the Transit Gateway resource.


Examples Output:
================



Creating a Resource Access Manager resource:
-------------------------------------------

- The following will creat a Transit Gateway Resource, the ARN listed is the Transit Gateway ARN (well an altered version)
::

 (python36) [da@scrap ~]$ aws ram create-resource-share --name typc-setup  --resource-arns arn:aws:ec2:us-west-2:xxxxxxxxxxx:transit-gateway/tgw-03e59dafb0e4e761c  --principals xxxxxxxxxxx
 {
    "resourceShare": {
        "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/ecb493f2-0109-28b6-f0e8",
        "name": "typc-setup",
        "owningAccountId": "xxxxxxxxxx",
        "allowExternalPrincipals": true,
        "status": "ACTIVE",
        "creationTime": 1551152448.054,
        "lastUpdatedTime": 1551152448.054
    }
 } 




Listing of  Resource Access Manager shares created:
---------------------------------------------------
::

 (python36) [da@scrap ~]$ aws ram get-resource-shares --resource-owner SELF
 {
    "resourceShares": [
        {
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/8ab484ba-182b-3907-5ad2",
            "name": "tgwait-ram",
            "owningAccountId": "xxxxxxxxxx",
            "allowExternalPrincipals": true,
            "status": "ACTIVE",
            "creationTime": 1550641803.391,
            "lastUpdatedTime": 1550641803.391
        },
        {
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/c0b484ba-5df7-752b-00ab",
            "name": "my-secret-transit-hub",
            "owningAccountId": "xxxxxxxxxx",
            "allowExternalPrincipals": true,
            "status": "ACTIVE",
            "tags": [
                {
                    "key": "Name",
                    "value": "my-secret-name"
                }
            ],
            "creationTime": 1550641839.16,
            "lastUpdatedTime": 1550641839.16
        }
    ]
 } 



Associated Principles:
---------------------
- Gets the associations for the specified Principle share
::


 python36) [da@scrap ~]$ aws ram get-resource-share-associations --association-type PRINCIPAL
 {
    "resourceShareAssociations": [
        {
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/8ab484ba-182b-3907-5ad2",
            "associatedEntity": "xxxxxxx",
            "associationType": "PRINCIPAL",
            "status": "ASSOCIATED",
            "creationTime": 1550641803.391,
            "lastUpdatedTime": 1550642741.292,
            "external": true
        },
        {
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/8ab484ba-182b-3907-5ad2",
            "associatedEntity": "xxxxxxxxxx",
            "associationType": "PRINCIPAL",
            "status": "ASSOCIATED",
            "creationTime": 1550641803.391,
            "lastUpdatedTime": 1550642898.17,
            "external": true
        },

Associated Resources:
---------------------

- Gets the associations for the specified Resources share

::


 (python36) [drivera@scrappy-aws ~]$ aws ram get-resource-share-associations --association-type RESOURCE{

 {
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/8ab484ba-182b-3907-5ad2",
            "associatedEntity": "arn:aws:ec2:us-west-2:xxxxxxxxxxx:transit-gateway/tgw-03e59da",
            "associationType": "RESOURCE",
            "status": "ASSOCIATED",
            "creationTime": 1550641803.391,
            "lastUpdatedTime": 1550641803.834,
            "external": false
        },
        {
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/c0b484ba-5df7-752b-00ab",
            "associatedEntity": "arn:aws:ec2:us-west-2:xxxxxxxxxxx:transit-gateway/tgw-03e59da",
            "associationType": "RESOURCE",
            "status": "ASSOCIATED",
            "creationTime": 1550641839.16,
            "lastUpdatedTime": 1550641839.585,
            "external": false
        }
    ]
}


List Associated and Pending Resource Requests:
----------------------------------------------

::

 (python36) [da@scrap ~]$ aws ram get-resource-share-invitations
 {
    "resourceShareInvitations": [
        {
            "resourceShareInvitationArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share-invitation/a0b484ba-18a5-b293-8101",
            "resourceShareName": "tgwait-ram",
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxx:resource-share/8ab484ba-182b-3907-5ad2",
            "senderAccountId": "xxxxxxxxxx",
            "receiverAccountId": "xxxxxxxxxxx",
            "invitationTimestamp": 1550642658.5,
            "status": "ACCEPTED"
        },
        {
            "resourceShareInvitationArn": "arn:aws:ram:us-west-2:xxxxxxxxxxxxx:resource-share-invitation/xxxx-xxxx-xxxx-xxx-xxxxxxx",
            "resourceShareName": "tvpc-setup",
            "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxx:resource-share/1ab493de-0109-1e01-932f",
            "senderAccountId": "xxxxxxxxxxxx",
            "receiverAccountId": "xxxxxxxxxx",
            "invitationTimestamp": 1551150628.143,
            "status": "PENDING"
        }
    ]
 }


Accepting Invitation:
---------------------

- The process of accepting an invitation from a target account

::


 (python36) [da@scrap ~]$ aws ram accept-resource-share-invitation --resource-share-invitation-arn arn:aws:ram:us-west-2:xxxxxxxx:resource-share-invitation/xxxxxx-xxxx-xxxx-xxxx-xxxxxxx
 {
    "resourceShareInvitation": {
        "resourceShareInvitationArn": "arn:aws:ram:us-west-2:xxxxxxxx:resource-share-invitation/d4b493e4-xxxx-4ab1-ac90-f61d3xxxxx",
        "resourceShareName": "tvpc-setup",
        "resourceShareArn": "arn:aws:ram:us-west-2:xxxxxxxxxxxx:resource-share/1ab493de-xxxx-1e01-932f-xxxxxxx",
        "senderAccountId": "xxxxxxxxxxxxx",
        "receiverAccountId": "xxxxxxxxxxxxx",
        "invitationTimestamp": 1551151245.343,
        "status": "ACCEPTED"
    }



