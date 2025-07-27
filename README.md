# Automated-Cloud-Incident-Response

This is a project that automates the containment and collectiong of forensic material for a compromised EC2 instance. It is an automated incident response system for AWS that:
1. Detects a "hacked" EC2 instance. This is simulated using a fake GuardDuty alert.
2. Isolates the instance by blocking all network traffic, incoming and outgoing.
3. Captures forensic evidence by taking a snapshot of the disk and extracting the metadata.
4. Saves evidence to S3

# Features
**Auto-containment**: Isolates instance via Security Group
**Evidence Preservation**: Stores snapshot/metadata in S3

# Architecture
