# Automated Blog Generation and S3 Storage using AWS Bedrock and Lambda

This project provides a serverless implementation of blog generation using AWS Bedrock with Mistral Large model and stores the generated blogs in an Amazon S3 bucket.

## Features
- Generate blogs based on a given topic using AWS Bedrock.
- Save the generated blogs in an S3 bucket with a timestamped filename.
- Expose an HTTPS endpoint for seamless integration with other applications.

## Deployment Steps

### 1. Install Required Python Libraries
Install the required dependencies inside a `python/` directory using the following command:
```bash
pip install boto3 -t python/
```
This installs the `boto3` library in a folder named `python/`, which is necessary for AWS Lambda.

### 2. Create Deployment Package
After installing the dependencies, compress the `python/` directory into a ZIP file for deployment:
```bash
zip -r python.zip python/
```

### 3. Upload and Deploy
- Upload the `python.zip` file to your Lambda function via the AWS Management Console or AWS CLI.
- Deploy the Lambda function to handle API requests.

## Testing the Endpoint
The deployed Lambda function is accessible via the following HTTPS endpoint:
```
https://hz8dh66894.execute-api.us-east-1.amazonaws.com/devenvronment/blog-generation
```

### Request Format
To test the endpoint, use a tool like Postman or cURL. Set the HTTP method to `POST` and provide the following payload in the body (set Content-Type to `application/json`):
```json
{
    "blog_topic": "AI vs HUMANS Who will win the life race??"
}
```

### Response
On successful execution, the endpoint will return:
- The generated blog content.
- The S3 location where the blog is stored.

Example response:
```json
{
    "message": "Blog Generation is completed",
    "blog_content": "Here is the generated blog content...",
    "s3_location": "s3://awsbedrockcourse04/blog-output/20231221_153045.txt"
}
```

## Files
- **Lambda Function Code**: Contains the logic to generate a blog using AWS Bedrock and save it to S3.
- **Deployment Package**: Includes the required dependencies (e.g., `boto3`) in `python.zip`.

## Tools Used
- **AWS Bedrock**: For blog generation using the Mistral Large model.
- **Amazon S3**: To store the generated blogs.
- **AWS Lambda**: To execute the serverless application logic.
- **Postman**: For testing the deployed API.

## Notes
- Ensure your Lambda function has the required IAM permissions for accessing Bedrock and S3.
- Update the S3 bucket name and other configurations in the Lambda code as necessary.

## Support
For questions or issues, please create a GitHub issue or contact the project maintainer.

