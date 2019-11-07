from flask import Blueprint, render_template, request
import os
import time
import boto3
import json

from app.models import EditableHTML

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)


@main.route('/sign-s3/')
def sign_s3():
    # Load necessary information into the application
    TARGET_FOLDER = 'json/'
    S3_REGION = 'us-east-2'
    S3_BUCKET = os.environ.get('S3_BUCKET')

    # Load required data from the request
    pre_file_name = request.args.get('file-name')
    file_name = ''.join(pre_file_name.split('.')[:-1]) + \
                str(time.time()).replace('.',  '-') + '.' + \
                ''.join(pre_file_name.split('.')[-1:])
    file_type = request.args.get('file-type')

    # Initialise the S3 client
    s3 = boto3.client('s3',
                      region_name=S3_REGION,
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
                      )

    # Generate and return the presigned URL
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=TARGET_FOLDER + file_name,
        Fields={
            "acl": "public-read",
            "Content-Type": file_type
        },
        Conditions=[{
            "acl": "public-read"
        }, {
            "Content-Type": file_type
        }],
        ExpiresIn=60000)

    # Return the data to the client
    return json.dumps({
        'data':
            presigned_post,
        'url_upload':
            'https://%s.%s.%s.amazonaws.com' % (S3_BUCKET, 's3', S3_REGION),
        'url':
            'https://%s.%s.%s.amazonaws.com/json/%s' % (S3_BUCKET, 's3', S3_REGION, file_name)
    })
