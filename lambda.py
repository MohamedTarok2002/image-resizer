from PIL import Image
import io
import boto3
import json

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get the bucket and file name from the S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        # Download the image from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        image_content = response['Body'].read()

        # Open the image with Pillow
        image = Image.open(io.BytesIO(image_content))

        # Resize the image (e.g., to 800x600 pixels)
        resized_image = image.resize((800, 600), Image.Resampling.LANCZOS)

        # Save the resized image to a bytes buffer
        output = io.BytesIO()
        resized_image.save(output, format=image.format)
        output.seek(0)

        # Upload the resized image back to S3 with a new key
        new_key = f"resized/{key}"  # Store in a 'resized' folder
        s3_client.put_object(Bucket=bucket, Key=new_key, Body=output)

        return {
            'statusCode': 200,
            'body': json.dumps(f'Image {key} resized and uploaded as {new_key} successfully!')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }