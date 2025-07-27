import boto3
import json
import datetime
import os

def lambda_handler(event, context):
    # Create EC2 and S3 clients
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')

    # Extract instance ID from the incoming GuardDuty-style event
    instance_id = event.get('detail', {}).get('resource', {}).get('instanceDetails', {}).get('instanceId', 'i-badbadbad')

    # Step 1: Isolate the instance by modifying its security group to use the Isolation SG
    try:
        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[os.environ['ISOLATION_SG']]  # Environment variable passed via CloudFormation
        )
        print(f"Isolated instance {instance_id}")
    except Exception as e:
        print(f"Isolation failed: {str(e)}")

    # Step 2: Create snapshots of all attached EBS volumes for forensics
    snapshot_ids = []
    try:
        volumes = ec2.describe_volumes(
            Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}]
        ).get('Volumes', [])
        
        for vol in volumes:
            snapshot = ec2.create_snapshot(VolumeId=vol['VolumeId'])
            snapshot_ids.append(snapshot['SnapshotId'])
            print(f"Created snapshot: {snapshot['SnapshotId']}")
    except Exception as e:
        print(f"Snapshot failed: {str(e)}")

    # Step 3: Store forensic metadata (instance ID, snapshot IDs, timestamp) into S3
    try:
        metadata = {
            "instance_id": instance_id,
            "snapshots": snapshot_ids,
            "timestamp": str(datetime.datetime.now()),
            "status": "Success" if snapshot_ids else "Partial"
        }
        s3.put_object(
            Bucket=os.environ['S3_BUCKET'],
            Key=f"{instance_id}/metadata.json",
            Body=json.dumps(metadata)
        )
        print(f"Uploaded metadata to S3")
    except Exception as e:
        print(f"S3 upload failed: {str(e)}")

    # Return a response (useful for testing/debugging)
    return {
        "instance_id": instance_id,
        "snapshots": snapshot_ids,
        "s3_location": f"s3://{os.environ['S3_BUCKET']}/{instance_id}/metadata.json"
    }
