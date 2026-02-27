import json
import boto3
import base64
import uuid
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

TABLE_NAME = "GuestbookEntries"
BUCKET_NAME = "digital-guestbook-media-awm"
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/360774677961/GuestbookEntryQueue"

def lambda_handler(event, context):

    # CORS headers (required for frontend)
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }

    try:
        body = json.loads(event["body"])

        name = body.get("name")
        message = body.get("message")
        image_data = body.get("image")
        event_id = body.get("event_id", "default-event")

        entry_id = str(uuid.uuid4())
        timestamp = int(time.time())
        media_url = None

        # Upload image to S3 if provided
        if image_data:
            image_bytes = base64.b64decode(image_data)
            object_key = f"{entry_id}.jpg"

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=object_key,
                Body=image_bytes,
                ContentType="image/jpeg"
            )

            media_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"

        # Store data in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                "EventID": event_id,
                "EntryTimestamp": str(timestamp),
                "EntryID": entry_id,
                "Name": name,
                "Message": message,
                "MediaURL": media_url,
                "SubmittedAt": datetime.utcnow().isoformat()
            }
        )

        # Send event to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "event_id": event_id,
                "entry_id": entry_id,
                "name": name,
                "timestamp": timestamp
            })
        )

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({
                "message": "Entry submitted successfully!"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({
                "error": str(e)
            })
        }
