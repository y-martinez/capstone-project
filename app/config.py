import os

S3_BUCKET                 = os.environ.get("AWS_S3_NAME")
S3_KEY                    = os.environ.get("AWS_KEY")
S3_SECRET                 = os.environ.get("AWS_SECRET")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

AWS_REGION                = 'us-west-2'
SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 8000