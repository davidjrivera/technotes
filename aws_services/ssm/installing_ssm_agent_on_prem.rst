Installing SSM Agent On-Prem
============================


What is ssm-agent
-----------------
- component of AWS systems manager
- lightweight agent installed on servers communicates with aws systems manager service
- installs on servers running on AWS EC2 or in on-premises data center
- enables us to automate maintenance and deployment tasks

  - create resource groups
  - instance inventory
  - apply patches, updates 
  - configuration changes across resource groups
  - run commands
  - open sessions

- provides amazon-ssm-agent deamon which runs on managed instances
- available from AWS package repo on S3 for most major distros

  - https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
  - https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb


What is a SSM managed instance
------------------------------

- any Amazon EC2 instance or on-premises server in your hybrid 
  environment that has been configured for Systems Manager
- SSM instance Id is different for on-prem vs. EC2

  - EC2:     i-XXXXXXXXXXXXXXX
  - On-prem: mi-XXXXXXXXXXXXXXX


What is a managed instance activation
-------------------------------------

- security credential which provides authentication and access tokens for
  ssm-agent running in on-prem hosts to connect to SSM service (kinda similar
  to IAM access key, or EC2 profile)
- consists of

  - activation id
  - activation code

- requires IAM role which allows on-prem ssm-agent to interact with SSM
- available to use for instance registration for limited time only

  - activation expiration does not interrupt existing registrations
  - default is 24 hours
  - max is 30 days

- a single activation can be used to register multiple instances

  - default is one


Installing SSM-Agent
--------------------

Steps:

- create ssm activation
- install ssm-agent package
- run ssm-agent registration
- restart ssm-agent service


Install using shell
*******************
::

  ssm/bash> cat create_ssm_agent_activation.sh
  #!/bin/bash

  # generate a activation id and key

  ACTIVATION_NAME=$1
  INSTANCE_ROLE=service-role/AmazonEC2RunCommandRoleForManagedInstances

  aws ssm create-activation \
    --description $ACTIVATION_NAME \
    --default-instance-name $ACTIVATION_NAME \
    --iam-role $INSTANCE_ROLE

  ssm/bash> ./create_ssm_agent_activation.sh my_activation
  {
    "ActivationId": "db0eec70-84d9-48cc-84ae-52df9e707802",
    "ActivationCode": "AxWEDErIw6nGfXK0bNXj"
  }

  ssm/bash> cat ssm_agent_setup.sh
  #!/bin/bash
  
  [ $# -ge 2 ] || exit 1
  
  ActivationID=$1
  ActivationCode=$2
  Region=us-west-2

  sudo yum install https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
  sudo stop amazon-ssm-agent
  sudo amazon-ssm-agent -register -code $ActivationCode -id $ActivationID -region $Region
  sudo start amazon-ssm-agent


  ssm/bash> scp ssm_agent_setup.sh ashley@awsscrum-lnx2:~/
  ssm/bash> ssh ashley@awsscrum-lnx2
  [ashley@awsscrum-lnx2 ~]$ sudo ./ssm_agent_setup.sh db0eec70-84d9-48cc-84ae-52df9e707802 AxWEDErIw6nGfXK0bNXj



Install using ansible
*********************

create activation and post it to SSM paramater store as encrypted string::

  ssm/boto> head make_ssm_activation.py
  #!/usr/bin/env python
  '''
  Creates ssm activation for a single host and puts activation id/code into
  ssm paramater store as 'SecretString'.
  
  Usage:
      python create_ssm_activation.py <hostname>
      aws ssm get-parameter --name /activation/<hostname> --with-decryption
  
  ssm/boto> ./make_ssm_activation.py awsscrum-lnx1
  Version: 1


install_ssm_agent ansible playbook::


  ssm/ansible/playbooks/install_ssm_agent> cat install_ssm_agent.yml
  ---
  # Usage:
  # ansible-playbook -i inventory -e "ssm_param_name=<param_name>" install_ssm_agent.yml
  
  # This playbook makes use of the following plugins and roles:
  #
  #   ansible plugin to query SSM parameter store
  #   https://docs.ansible.com/ansible/2.5/plugins/lookup/aws_ssm.html
  #
  #   ansible role to install and register ssm-agent
  #   https://github.com/dhoeric/ansible-aws-ssm
  
  
  - hosts: testservers
    remote_user: ashley
    become: yes
    vars:
      region: "us-west-2"
      activation: "{{ lookup('aws_ssm', '{{ ssm_param_name }}') }}"
    roles:
      - role: ansible-aws-ssm
        vars:
          aws_ssm_activation_id: "{{ activation['ActivationId'] }}"
          aws_ssm_activation_code: "{{ activation['ActivationCode'] }}"
          aws_ssm_ec2_region: "{{ region }}"

  ssm/ansible/playbooks/install_ssm_agent> find . -maxdepth 3
  .
  ./README.rst
  ./inventory
  ./install_ssm_agent.yml
  ./roles
  ./roles/ansible-aws-ssm
  ./roles/ansible-aws-ssm/tests
  ./roles/ansible-aws-ssm/files
  ./roles/ansible-aws-ssm/README.md
  ./roles/ansible-aws-ssm/defaults
  ./roles/ansible-aws-ssm/meta
  ./roles/ansible-aws-ssm/.git
  ./roles/ansible-aws-ssm/handlers
  ./roles/ansible-aws-ssm/.travis.yml
  ./roles/ansible-aws-ssm/vars
  ./roles/ansible-aws-ssm/tasks


running install_ssm_agent playbook::

  ssm/ansible/playbooks/install_ssm_agent> cat inventory
  [testservers]
  awsscrum-lnx1
  
  ssm/ansible/playbooks/install_ssm_agent> ansible-playbook -i inventory -e "ssm_param_name=/activation/awsscrum-lnx1" install_ssm_agent.yml
  
  PLAY [testservers] *************************************************************
  
  TASK [Gathering Facts] *********************************************************
  ok: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Get CPU architecture] **********************************
  ok: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Change URL destination for 32bit arch] *****************
  skipping: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Install rpm file for Redhat Family (Amazon Linux, RHEL, and CentOS) 32/64-bit] ***
  changed: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Install deb file for Debian family 32/64-bit] **********
  skipping: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Check if node is registered] ***************************
  ok: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Register managed instance] *****************************
  skipping: [awsscrum-lnx1]
  
  TASK [ansible-aws-ssm : Register to service] ***********************************
  skipping: [awsscrum-lnx1]
  
  PLAY RECAP *********************************************************************
  awsscrum-lnx1              : ok=4    changed=1    unreachable=0    failed=0



tag on-prem instance with SSM
-----------------------------
::

  aws ssm describe-instance-information | egrep "InstanceId|ComputerName" | grep -B1 csgappt01
  
  HOSTNAME=csgappt01
  ID=mi-0632f5beb972bd5f4
  
  aws ssm add-tags-to-resource \
    --resource-type ManagedInstance \
    --tags \
      Key=Name,Value=${HOSTNAME} \
      Key=ucop:application,Value=migration \
      Key=ucop:environment,Value=poc \
      Key=ucop:service,Value=ait \
    --resource-id ${ID}

  aws ssm list-tags-for-resource \
    --resource-type ManagedInstance \
    --resource-id $ID



Where do we go from here
------------------------
   
- tag replicated AMI based on managed instance tags

  - automate AMI tagging via cloudwatch events and lambda

- use tags to configure placement and networking during migration
- use tags to create ssm resource groups 

  - manage migration of entire stacks

- tag ec2 instances based on AMI tags after migration
- can we use ssm to create sms replication jobs?


Things learned
----------------

- we cannot migrate sles11 VM, because migration tools do not support reiserfs
- we should make sure hostname and vm name match prior to replication setup

- we will need to manage rep job artifacts

  - AMI proliferation

    - tag by hostname of source VM

  - snapshots

    - delete all repjob snaps except most recent

  - delete repjobs after instance migration complete
  - tag AMI with migrationStatus
  - retain AMI for used completed migration

- not trivial to match VM attributes to migrated EC2 instances

  - multiple sources of metadata must be queried:

    - ssm managedInstance
    - replication job
    - AMI
    - ec2 instance
