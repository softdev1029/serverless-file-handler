import os
import boto3
from os import path

s3 = boto3.resource('s3')

VERSION = 1
MADE_TIME = '09-27 09:55 PM'

def handler(event, context):

  # Read options from the event.
  print("<<< <<< <<< Starting to process S3 Add Event (Version: {}, Made Time: {})".format(VERSION, MADE_TIME))
  print(event)

  try:
    bucketName = event['Records'][0]['s3']['bucket']['name']
    srcKey = event['Records'][0]['s3']['object']['key']
  except Exception as e:
    print("Failed reading options. {} >>> >>> >>>".format(e))
    return

  print("Reading {}/{}".format(bucketName, srcKey))

  # Check if the object is from the input folder
  if srcKey.startswith('Incoming/') != True:
    print("We only process the objects from Incoming/ folder. >>> >>> >>>")
    return

  # Check if the object is just the input folder
  if srcKey.endswith('Incoming/') != True:
    print("We don't process the Incoming/ folder itself. >>> >>> >>>")
    return

  # destination file
  destKey = srcKey.replace('Incoming', 'Processed')

  # Grabs the source file
  try:
    obj = s3.Object(
        bucket_name=bucketName,
        key=srcKey,
    )
    obj_body = obj.get()['Body'].read()
    print("File [{}], content=[{}]".format(srcKey, obj_body))
  except Exception as e:
    print("Failed reading the source file. {} >>> >>> >>>".format(e))
    return

  # Delete the original file from the input bucket
  try:
    obj.delete()
  except Exception as e:
    print("Failed deleting the original file. {}".format(e))

  # Copy it to the destination folder
  try:
    # Uploading the file
    obj = s3.Object(
      bucket_name=bucketName,
      key=destKey,
    )
    obj.put(Body=obj_body)

    print("Moved... {}/{}".format(bucketName, destKey))
  except Exception as e:
    print("Failed moving {} file={}".format(e, destKey))

if __name__ == "__main__":
  handler('', '')