import boto3  
import json
import os
import time
import io
import redis


ld = rk = boto3.client('lambda', aws_access_key_id='AKIAIVAQCCTZIP3HEUIQ', aws_secret_access_key='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', region_name='us-west-2')

response = ld.invoke(FunctionName="plateDetect")
time.sleep(10)
#print(json.loads(response['Payload'].read()))
print response
print("\n")
