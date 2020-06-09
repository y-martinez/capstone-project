#!/usr/bin/env python3

import boto3,json
from flask import Flask, render_template, request,redirect,flash,session,url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence","AgeRange")

app = Flask(__name__)
app.config.from_object('config')

#TODO: Test the linter
# Connect to the s3 service
rekognition = boto3.client("rekognition",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"],
    region_name=app.config["AWS_REGION"])

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"],
    region_name=app.config["AWS_REGION"]
)

def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file,bucket,acl="public-read"):

    s3.upload_fileobj(
        file,
        bucket,
        file.filename,
        ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type
        }
    )

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)

def detect_faces(file,bucket):

    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": file.filename,
            }
        },
        Attributes=['ALL'],
    )
    result = '['
    for face in response['FaceDetails']:
        result += '{'
        result +=  '"Face" : "{Confidence}%",'.format(**face)
        result += '"Age" : "{Low} to {High} years",'.format(**face['AgeRange'])
        # emotions
        for emotion in face['Emotions']:
            result += '"{Type}" : "{Confidence}%",'.format(**emotion)
        # quality
        for quality, value in face['Quality'].items():
            result += '"{quality}" : "{value}",'.format(quality=quality, value=value)
        # facial features
        for feature, data in face.items():
            if feature not in FEATURES_BLACKLIST:
                result += '"{feature}({data[Value]})" : "{data[Confidence]}%",'.format(feature=feature, data=data)
        result=result[:-1]
        result +='},'

    result=result[:-1]
    result +=']'
    return result

@app.route('/result')
def results():
    output =json.loads(session['output'])
    analized = json.loads(output['analized'])
    return render_template('result.html',img=output['img'],faces_analized=analized)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        if 'image_file' not in request.files:
            flash(message="Please upload a photo",category="error")
            return redirect('/')
 
        file = request.files['image_file']

        if file.filename == "":
            flash(message="Please upload a photo",category="error")
            return redirect('/')
        
        if file and allowed_files(file.filename):
            file.filename = secure_filename(file.filename)
            file_uploaded = upload_file_to_s3(file,app.config['S3_BUCKET'])
            file_analized = detect_faces(file,app.config['S3_BUCKET'])

        output = {
            'img':file_uploaded,
            'analized':file_analized
        }
        session['output'] = json.dumps(output)

        flash(message="Success image analized",category="success")
        return redirect(url_for('results'))

    flash(message="An error ocurred",category="error")
    return redirect(url_for('index'))


@app.route('/analize',methods=["GET"])
def analize():
    return render_template('index.html')

@app.route('/',methods=["GET"])
def index():
    return '<h1>Hello, Udacity! this is my final Capstone project</h1>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])