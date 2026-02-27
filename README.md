# AWS Serverless Digital Guestbook

## Overview
Designed and deployed a fully serverless guestbook application using AWS services.  
Users submit their name, message, and optional image through a REST API endpoint.

The system processes requests through API Gateway, Lambda, DynamoDB, S3, and SQS.

## Architecture
![Architecture Diagram](architecture-diagram.png)

## AWS Services Used
- API Gateway – REST API endpoint
- Lambda – Serverless compute layer
- DynamoDB – NoSQL database for guest entries
- S3 – Image storage
- SQS – Asynchronous message queue
- CloudWatch – Logging and monitoring
- IAM – Role-based access control

## Workflow
1. User submits form data.
2. API Gateway triggers Lambda.
3. Lambda:
   - Stores text data in DynamoDB.
   - Uploads image to S3.
   - Sends message to SQS.
4. CloudWatch logs track execution.

## Engineering Concepts Demonstrated
- Serverless Architecture
- Event-Driven Design
- Least-Privilege IAM
- Asynchronous Messaging
- Distributed System Monitoring

## Screenshots

### API Gateway
![API Gateway](screenshots/api-gateway.png)

### Lambda
![Lambda](screenshots/lambda.png)

### DynamoDB
![DynamoDB](screenshots/dynamodb.png)

### S3
![S3](screenshots/s3.png)

### SQS
![SQS](screenshots/sqs.png)

### Postman Test
![Postman](screenshots/postman.png)

## Demo Video
🎥 (Paste YouTube unlisted link here)
