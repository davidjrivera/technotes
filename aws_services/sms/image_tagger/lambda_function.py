# Sample Lambda function to launch add tags to all AMI ID's created from a 
# Server Migration Service replication job

import boto3

# main function
def lambda_handler(event, context):

    # create an ec2 client
    ec2 = boto3.client('ec2', region_name=event['region'])
    
    # match any event that returns an ami-id	
    if 'ami-id' in event['detail']:
        imageId = event['detail']['ami-id']

        # launch instance from the AMI ID
        ec2.run_instances(
            ImageId=imageId,
            MaxCount=123,
            MinCount=1,
            InstanceType='t2.micro'
        )
        print 'launched instance with ami id: ' + imageId
    else:
        pass
