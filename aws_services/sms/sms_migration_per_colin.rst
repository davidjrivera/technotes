How to Deploy Linux boxen in the Boneyard
=========================================

adapted from confluence page https://confluence.ucop.edu/display/OMG/How+to+Deploy+Linux+boxen+in+the+Boneyard

Created by Unknown User (cothomps), last modified on Aug 17, 2017 Go to start of metadata

This doc is a work in progress.  What it says might hold some element of truth.  Then again, it might not.

Step-by-step guide
------------------
- If migrating a host from VMWare, set up a replication job in the Server Migration Service (AWS Console) to create an AMI based on the VM.

- Once the migration job is complete, find the job in the SMS console, and click the deploy button next to the AMI from that job.

- At this point, you're in the business of deploying an EC2 instance from an AMI, and you need to know the usual stuff: CPUs, RAM, disks, etc.  Whatever you end up selecting, don't overlook the final step where you give the instance a tag called "Name" (has to be a capital N) with a value of whatever the hostname is.  Also, be careful about the security group because you can't change it later.  You can only add rules to existing security groups, which affect all hosts that use that security group, so be sure to get it right here.

- Once the instance is running and you can SSH in, patch it.

- Submit a ticket to NOC for DNS.

- Create puppet node manifest and hiera data (currently only unxpupp01 works, so use it)
- Add centrify zone info and meta data to hiera

- Run new_ip and new_vm scripts, run puppet and sign cert


