#!/bin/bash

[ $# -ge 2 ] || exit 1

ActivationID=$1
ActivationCode=$2
Region=us-west-2

sudo yum install https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
sudo stop amazon-ssm-agent
sudo amazon-ssm-agent -register -code $ActivationCode -id $ActivationID -region $Region
sudo start amazon-ssm-agent

