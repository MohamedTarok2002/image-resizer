# Image Resizer with AWS Lambda

## Description
A serverless application that automatically resizes images uploaded to an S3 bucket. When an image is uploaded, an AWS Lambda function triggers, resizes it to 800x600 pixels using Pillow, and saves it in a `resized/` folder.

## Prerequisites
- AWS account with Lambda and S3 access
- Python 3.x installed locally
- AWS CLI (optional, for deployment)
- for my project i used python 3.11 and for pillow i add layer for version arn:
arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-Pillow:7



## Installation
1. Create an S3 bucket (e.g., `my-image-bucket`).
2. Set up a Lambda function:
   - Runtime: Python 3.9
   - Upload the code with Pillow dependency (see below).
3. Add an S3 trigger:
   - Event type: `s3:ObjectCreated:*`
   - Link to your Lambda function.
4. Package dependencies:
   
    for my project i used python 3.11 and for pillow i add layer   for version arn:
arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-Pillow:7

or 
   - Run `pip install pillow -t .` in your project folder.
   - Zip the folder with `lambda_function.py` and upload to Lambda.

## Usage
1. Upload an image to your S3 bucket (e.g., `photo.jpg`).
2. Check the `resized/` folder for the output (e.g., `resized/photo.jpg`).

## Code
```python
from PIL import Image
import io
import boto3
import json

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        response = s3_client.get_object(Bucket=bucket, Key=key)
        image_content = response['Body'].read()
        image = Image.open(io.BytesIO(image_content))
        resized_image = image.resize((800, 600), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        resized_image.save(output, format=image.format)
        output.seek(0)
        new_key = f"resized/{key}"
        s3_client.put_object(Bucket=bucket, Key=new_key, Body=output)
        return {'statusCode': 200, 'body': json.dumps(f'Image {key} resized and uploaded as {new_key} successfully!')}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}
