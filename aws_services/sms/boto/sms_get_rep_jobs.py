import sys
import boto3
from organizer.utils import yamlfmt


if len(sys.argv) > 1:
    vmname = sys.argv[1]
else:
    vmname = None

client = boto3.client('sms')


# load up all replication jobs

response = client.get_replication_jobs()
jobs = response['replicationJobList']
while 'nextToken' in response:
    response = client.get_replication_jobs(
        nextToken=response['nextToken']
    )  
    jobs += response['replicationJobList']
#print(yamlfmt(jobs))



# display failed rep jobs
failed_jobs = [job for job in jobs if job['state'] == 'Failed']
#print(yamlfmt(failed_jobs))

failed_listing = [dict(vmName=job['vmServer']['vmName'], statusMessage=job['statusMessage']) for job in failed_jobs]
#print(yamlfmt(failed_listing))
if vmname:
    print(yamlfmt([job for job in failed_jobs if job['vmServer']['vmName'] == vmname]))
else:
    print(yamlfmt(failed_listing))



