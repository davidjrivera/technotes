#!/bin/bash

# generate a activation id and key

ACTIVATION_NAME=$1
INSTANCE_ROLE=service-role/AmazonEC2RunCommandRoleForManagedInstances

aws ssm create-activation \
  --description $ACTIVATION_NAME \
  --default-instance-name $ACTIVATION_NAME \
  --iam-role $INSTANCE_ROLE




