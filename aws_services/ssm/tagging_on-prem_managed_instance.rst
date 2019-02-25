Tagging On-Prem VMs with SSM
============================

VM must be running SSM Agent.

Get the SSM managedInstanceId for your instance::

  aws ssm describe-instance-information

Retrieve tags for on-prem instance::

  aws ssm list-tags-for-resource \
    --resource-type ManagedInstance \
    --resource-id mi-1234455667788

example::
  technotes/aws/ssm> aws ssm list-tags-for-resource --resource-type ManagedInstance --resource-id mi-008eebc6e82e4c3f1
  {
      "TagList": [
          {
              "Key": "ucop:application",
              "Value": "migration"
          },
          {
              "Key": "Name",
              "Value": "awsscrum-lnx1"
          }
      ]
  }


Set tags on a managed instance::

  aws ssm add-tags-to-resource \
    --resource-type ManagedInstance \
    --resource-id  mi-08032710dee55bc93 \
    --tags \
      Key=Name,Value=aigtest02 \
      Key=ucop:application,Value=migration \
      Key=ucop:environment,Value=poc \
      Key=ucop:service,Value=ait
