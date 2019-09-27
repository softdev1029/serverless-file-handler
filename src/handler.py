import os
import boto3
from os import path

s3 = boto3.resource('s3')

DST_BUCKET = "file-processed2"
TMP_DIR = "/tmp"
VERSION = 1
MADE_TIME = '09-27 09:25 AM'

def handler(event, context):

  # Read options from the event.
  print("<<< <<< <<< Starting to process S3 Add Event (Version: {}, Made Time: {})".format(VERSION, MADE_TIME))
  print(event)

  try:
    srcBucket = event['Records'][0]['s3']['bucket']['name']
    srcKey = event['Records'][0]['s3']['object']['key']
  except Exception as e:
    print("Failed reading options. {} >>> >>> >>>".format(e))
    return

  print("Reading {}/{}".format(srcBucket, srcKey))

  # dst bucket
  dstBucket = DST_BUCKET
  dstKey = srcKey

  # Sanity check: validate that source and destination are different buckets.
  if (srcBucket == dstBucket) :
    print("Destination bucket must not match source bucket >>> >>> >>>")
    return

  # Grabs the source file
  try:
    obj = s3.Object(
        bucket_name=srcBucket,
        key=srcKey,
    )
    obj_body = obj.get()['Body'].read()
  except Exception as e:
    print("Failed downloading source file. {} >>> >>> >>>".format(e))
    return

  try:
    src_file = srcKey.replace('/', '-')
    src_name = src_file
    file = open(TMP_DIR + '/' + src_file, 'wb')
    file.write(obj_body)
    file.close()
  except Exception as e:
    print("Failed writing source file. {} : {} >>> >>> >>>".format(e, TMP_DIR + '/' + src_file))
    return

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
          bucket_name=dstBucket,
          key=file,
        )
        obj.put(Body=buffer)

        print("Uploaded... {}/{}".format(dstBucket, file))
      except Exception as e:
        print("Failed uploading {} file={}".format(e, file))
  print("Done all action >>> >>> >>>")

if __name__ == "__main__":
  main('', '')