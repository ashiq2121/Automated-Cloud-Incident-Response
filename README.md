# Automated-Cloud-Incident-Response

A serverless system that auto-isolate and captures forensic data for a compromised EC2 instance. 

It is an automated incident response system for AWS that:
1. Detects a "hacked" EC2 instance. This is simulated using a fake GuardDuty alert.
2. Isolates the instance by blocking all network traffic, incoming and outgoing.
3. Captures forensic evidence by taking a snapshot of the disk and extracting the metadata.
4. Saves evidence to S3

# Features
- **Auto-containment**: Isolates instance via Security Group
- **Disk Forensics**: Captures EBS snapshot
- **Evidence Logging**: Stores metadata in S3


# Architecture

# Deployment
1. Launch EC2 instance
2. Set up Isolation Security Group
3. Deploy CloudFormation template
4. Test with Lambda event

# Screenshots

- [Isolated Instance](
