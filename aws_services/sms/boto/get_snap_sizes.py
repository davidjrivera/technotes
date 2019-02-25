import boto3


client = boto3.client('ec2')


response = client.describe_snapshots(
    #nextToken='string',
)

snaps = response['Snapshots']
while 'nextToken' in response:
    response = client.describe_snapshots(
        nextToken=response['nextToken']
    )  
    snaps += response['Snapshots']

sizes = [snap['VolumeSize'] for snap in snaps]
print(len(sizes))
total_snap_size = sum(sizes)
print(total_snap_size)
