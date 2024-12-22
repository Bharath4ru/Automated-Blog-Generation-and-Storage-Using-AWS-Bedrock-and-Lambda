import boto3
import botocore.config
import json
from datetime import datetime

def blog_generate_using_bedrock(blogtopic: str) -> str:
    """
    Generates a blog using AWS Bedrock by invoking Mistral Large model.
    """
    prompt = f"""<s>[INST] Write a 100 words blog on the topic {blogtopic} [/INST]"""
    
    body = {
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50
    }
    
    try:
        # Initialize Bedrock client
        bedrock = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3})
        )
        
        # Invoke Mistral Large model
        response = bedrock.invoke_model(
            body=json.dumps(body),
            modelId="mistral.mistral-large-2402-v1:0",
            contentType="application/json",
            accept="application/json"
        )
        
        # Process the response
        response_content = json.loads(response['body'].read().decode('utf-8'))
        blog_details = response_content.get('outputs', [{}])[0].get('text', '')
        return blog_details
    
    except Exception as e:
        print(f"Error generating the blog: {e}")
        return ""

def save_blog_details_s3(s3_key: str, s3_bucket: str, generate_blog: str):
    """
    Saves the generated blog to an S3 bucket.
    """
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Blog saved to S3")
    except Exception as e:
        print(f"Error when saving the blog to S3: {e}")

def lambda_handler(event, context):
    """
    Lambda handler to generate a blog and save it to S3.
    """
    try:
        # Parse event data
        if isinstance(event.get('body'), str):
            event_body = json.loads(event['body'])
        else:
            event_body = event.get('body', {})
            
        blogtopic = event_body.get('blog_topic')
        if not blogtopic:
            return {
                'statusCode': 400,
                'body': json.dumps('blog_topic is required')
            }
            
        # Generate blog content
        generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)
        if generate_blog:
            # Save generated blog to S3
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            s3_key = f"blog-output/{current_time}.txt"
            s3_bucket = 'awsbedrockcourse04'
            save_blog_details_s3(s3_key, s3_bucket, generate_blog)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Blog Generation is completed',
                    'blog_content': generate_blog,
                    's3_location': f"s3://{s3_bucket}/{s3_key}"
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to generate blog content')
            }
            
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }
