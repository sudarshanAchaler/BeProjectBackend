import boto3
import os
from botocore.exceptions import ClientError
from django.conf import settings
import random

def uploadPostImage(file_name,object_name):
    return upload_file(file_name,"postImages/",object_name)

def uploadCoverImage(file_name,object_name):
    return upload_file(file_name,"coverImages/",object_name)

def uploadProfileImage(file_name,object_name):
    return upload_file(file_name,"profileImages/",object_name)


def upload_file(file_name,imageType,object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: error if there is one
    """

    # If S3 object_name was not specified, use file_name
    bucket = settings.AWS_S3_BUCKET_NAME
    hash = random.getrandbits(32)
    object_name = object_name + str(hash)
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        _ = s3_client.upload_fileobj(file_name, bucket, imageType+object_name,ExtraArgs={'ACL': 'public-read'})

    except ClientError as e:
        return e,None
    return None,"https://sudarshanbeproject.s3.ap-south-1.amazonaws.com/" + imageType+object_name