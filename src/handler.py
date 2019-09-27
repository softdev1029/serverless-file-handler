import os
import boto3
from os import path

s3 = boto3.resource('s3')

TMP_DIR = "/tmp"
VERSION = 1
MADE_TIME = '09-27 09:25 AM'

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

  # destination file
  destKey = srcKey.replace('Incoming', 'Processed')

  # Grabs the source file
  try:
    obj = s3.Object(
        bucket_name=bucketName,
        key=srcKey,
    )
    obj_body = obj.get()['Body'].read()
  except Exception as e:
    print("Failed downloading source file. {} >>> >>> >>>".format(e))
    return

  # Read the file content
  try:
    src_file = srcKey.replace('/', '-')
    src_name = src_file
    file = open(TMP_DIR + '/' + src_file, 'wb')
    file.write(obj_body)
    file.close()
  except Exception as e:
    print("Failed writing source file. {} : {} >>> >>> >>>".format(e, TMP_DIR + '/' + src_file))
    return

  # Delete the original file from the input bucket
  try:
    obj.delete()
  except Exception as e:
    print("Failed deleting the original file. {}".format(e))

  # Upload it to the destination bucket
  for file in os.listdir(TMP_DIR):
    if file.startswith(src_name):
      try:
        src_file = open(TMP_DIR + '/' + file, 'rb')
        buffer = src_file.read()
        print("File [{}], content=[{}]".format(file, buffer))
        os.remove(TMP_DIR + '/' + file)
        src_file.close()
      except Exception as e:
        print("Failed reading {} file={}".format(e, TMP_DIR + '/' + file))

      try:
        # Uploading the file
        obj = s3.Object(
          bucket_name=bucketName,
          key=file,
        )
        obj.put(Body=buffer)

        print("Uploaded... {}/{}".format(bucketName, file))
      except Exception as e:
        print("Failed uploading {} file={}".format(e, file))
  print("Done all action >>> >>> >>>")

if __name__ == "__main__":
  main('', '')