import sys
import re
import boto3
from organizer.utils import yamlfmt



if len(sys.argv) > 1:
    ami = sys.argv[1]
else:
    ami = None


ec2_client = boto3.client('ec2')
desc_re = re.compile(r'SMS ReplicationJobId = (.*) ReplicationRunId = .*')

response = ec2_client.describe_images(
    Owners=['self'],
)
#print(yamlfmt(response))

image_ids = [image['ImageId'] for image in response['Images']
    if desc_re.match(image['Description'])
]
print(yamlfmt(image_ids))

sms_job_ids = list({
    desc_re.match(image['Description']).group(1)
    for image in response['Images']
    if desc_re.match(image['Description'])
})
print(yamlfmt(sms_job_ids))

jobid_for_image = [
    dict(
        image_id=image['ImageId'], 
        sms_job_id=desc_re.match(image['Description']).group(1)
    )
    for image in response['Images']
    if desc_re.match(image['Description'])
]
print(yamlfmt(jobid_for_image))


sms_client = boto3.client('sms')
for image_map in jobid_for_image:
    print(image_map)
    try:
        response = sms_client.get_replication_jobs(
            replicationJobId=image_map['sms_job_id'],
        )
        vm_name = response['replicationJobList'][0]['vmServer']['vmName']
        print(vm_name)
    except:
        pass
    response = ec2_client.create_tags(
        #DryRun=True,
        Resources=[image_map['image_id']],
        Tags=[dict(
            Key='Name',
            Value=vm_name,
        )],
    )
    print(yamlfmt(response))

