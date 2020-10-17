import boto3
import json
import datetime
import os
import pprint

BUCKET_NAME = 'remos-raw-csv'
LOCATION = 'eu-north-1'
BUCKET_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:*"],
            "Resource": ["arn:aws:s3:::remos-raw-csv"]
        }
    ]
}
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))


# def s3_client():
#     s3 = boto3.client('s3')
#     """ :type : pyboto3.s3"""
#     return s3
#
#
# def create_bucket(bucket_name):
#     try:
#         return s3_client().create_bucket(
#             Bucket=bucket_name,
#             CreateBucketConfiguration={
#                 'LocationConstraint': 'eu-north-1'
#             }
#         )
#     except Exception as e:
#         print('Your previous request to create the named bucket succeeded and you already own it.')
#
#
# def list_bucket():
#     for bucket in s3_client().list_buckets()['Buckets']:
#         print(bucket['Name'])

def print_response(res, mess):
    now = datetime.datetime.now()
    print(now.strftime("%d-%m-%Y-%H:%M:%S"),
          f" ---- HTTP-code:{res['ResponseMetadata']['HTTPStatusCode']} ---- Message:{mess}")


class S3Object:
    def __init__(self, bucket_name, region):
        self.s3_client = boto3.client('s3')
        """:type :  pyboto3.s3"""
        try:
            response = self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationContraint': region
                }
            )
            print_response(response, 'bucket created')
        except:
            print('Your previous request to create the named bucket succeeded and you already own it.')

    def list_bucket(self):
        print('List buckets:')
        for bucket in self.s3_client.list_buckets()['Buckets']:
            print('-', bucket['Name'])

    def create_bucket_policy(self, policy):
        policy_string = json.dumps(policy)
        response = self.s3_client.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=policy_string
        )
        print_response(response, 'policy created')
        # print(json.dumps(response,sort_keys=True,indent=4))

    def update_bucket_policy(self, bucket_name, policy):
        policy_string = json.dumps(policy)
        response = self.s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_string
        )
        print_response(response, 'policy created')

    def delete_bucket(self, bucket_name):
        response = self.s3_client.delete_bucket(
            Bucket=bucket_name
        )
        print_response(response, 'bucket deleted')

    def upload_small_file(self, bucket, key):
        path = os.path.abspath(os.path.join(DATA_PATH, key))
        self.s3_client.upload_file(path, bucket, key)
        print(f'{key} uploaded to {bucket}')

    def list_file(self, bucket):
        response = self.s3_client.list_objects(
            Bucket=bucket,
        )
        print(f'Files in {bucket}:')
        for file in response['Contents']:
            print('-', file['Key'])

    def delete_file(self, bucket, key):
        response = self.s3_client.delete_object(
            Bucket=bucket,
            Key=key)
        print_response(response, f'{key} deleted from {bucket}')


if __name__ == '__main__':
    s3 = S3Object(BUCKET_NAME, LOCATION)
    s3.list_bucket()
    # s3.list_file(BUCKET_NAME)
    # s3.create_bucket_policy(BUCKET_POLICY)
    # s3.delete_bucket('trung-s3-2020-bucket-2')
    # s3.list_bucket()
    # s3.delete_file(BUCKET_NAME, 'kemi_raw.csv')
    s3.upload_small_file(BUCKET_NAME, 'kemi_raw.csv')  # TODO: go configure lambda function in AWS LAMBDA
