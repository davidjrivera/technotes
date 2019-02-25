AWS EC2 Infrastructure Backlog
==============================

Adapted from Ashley's AWS Infrastructure Backlog with just stuff specific
to EC2 management




EC2 Management in Legacy Data Center and elsewhere
--------------------------------------------------

- archetectural review

  - vpc/subnet layout
  - perimeter security
  - DNS/route53
  - loadbalancers

- ensure existing (on-prem) system mgmt tools work reliably

  - puppet
  - ansible
  - sccm
  - AD/Centrify
  - UIM

- ensure AWS system mgmt tools work reliably

  - ssm
  - nakivo
  - system log aggregation to s3

- PCSSC integration

  - control-m
  - goanywhere

- ec2 instance tagging

  - determine required tags
  - enforce tagging compliance
  - integration with CMDB

- security tools

  - idp
  - waf
  - firewall
  - siem/qRadar
  - ssl cert management

- Config Rules

  - ensure ebs volume encryption at rest
  - ensure ec2 instances built from compliant AMI
  - ensure ec2 instances are at current patch levels

- ec2 instance build process

  - intake workflow
  - build proceedure

    - automated instance builder tools
    - IP address assignment
    - DNS configuration

  - template AMIs

    - leveage Eric's Salami Factory AMI builder
    - template image requirements

      - tags
      - central logging config
      - OS hardening
      - AD access
      - system management agents

         - ssm
         - sccm
         - puppet


- maintain repository of UCOP standardized ec2 AMI
- develop SSM service to manage running ec2 instances



Guidelines for running EC2 instances in AWS (outside of boneyard)
-----------------------------------------------------------------

Avoid hosting applications on EC2 instances. But if you feel you must:

-  Devops will maintain base AMIs for an approved set of OS distributions.
   These AMI will be updated weekly.They include the following:

   -  SSM agent

   -  predefined instance policy for centralized logging

   -  basic security configuration

-  Developers deploy EC2 instances from one of the Devops managed AMI,
   ideally using userdata scripts to configure customization at launch
   time.

-  EC2 instances write system and application logs to S3.

-  EC2 instances should be stateless. Avoid attaching EFS or ELB
   volumes.

-  EC2 instances should be restarted weekly to avoid configuration drift
   and to apply OS updates.

-  EC2 instances run on private subnets and are not publicly routable.
   Access is via ELB.

-  No direct user access (``ssh``, ``rdp``) to running EC2 instances.

-  Any system management or configuration change is done via SSM or by
   updating the build scripts and relaunching.


