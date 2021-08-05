import os
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)


def get_s3_resource(*, endpoint_url, aws_access_key_id, aws_secret_access_key):
    try:
        s3_resource = boto3.resource(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        return s3_resource
    except Exception as e:
        logging.info(e)
        

def get_mother_root(directory):
    try:
        if directory.endswith("/") and len(directory) > 1:
            mother_root = directory.split("/")[-2]
        elif len(directory) > 1:
            mother_root = directory.split("/")[-1]
        else:
            mother_root = "/"
        return mother_root
    except Exception as e: 
        logging.error(e)


def upload(*, bucket_name, s3_resource, directory, ACL):
    try:
        bucket = s3_resource.Bucket(bucket_name)
        mother_root = get_mother_root(directory)
        count = 0
        print()
        print(f"Uploading file to {bucket_name}...")
        print()
        for dirname, dirs, files in os.walk(directory):
            for filename in files:
                dirname = dirname if dirname.endswith("/") else dirname + "/"
                object_name = dirname.split(mother_root)[-1][1:]
                file_path = dirname + filename
                object_name = object_name + filename
                with open(file_path, "rb") as file:
                    bucket.put_object(
                        ACL=ACL,
                        Body=file,
                        Key=object_name
                    )
                print(f"Uploaded '{object_name}'")
                count += 1
        print(f"{count} files uploaded.")
    except ClientError as e:
        logging.error(e)
        

def main():
    directory = input("Directory: ")
    endpoint_url = input("Endpoint URL: ")
    aws_access_key_id = input("AWS access key: ")
    aws_secret_access_key = input("AWS secret key: ")
    acl = input("ACL: ")
    bucket_name = input("Bucket name: ")
    
    s3_resource = get_s3_resource(
        endpoint_url=endpoint_url, 
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key,
    )
    upload(
        bucket_name=bucket_name,
        s3_resource=s3_resource, 
        directory=directory, 
        ACL=acl,
    )
    

if __name__ == "__main__":
    main()
    