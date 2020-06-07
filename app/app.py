#!/usr/bin/env python3

import boto3
from flask import Flask, render_template, request,redirect,flash,url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence","AgeRange")

app = Flask(__name__)
app.config.from_object('config')

# Connect to the s3 service
rekognition = boto3.client("rekognition", app.config["AWS_REGION"])
s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"]
)

def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file,bucket,acl="public-read"):
    try:

        s3.upload_fileobj(
            file,
            bucket,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)

def detect_faces(file,bucket, attributes=['ALL']):

    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": file.filename,
            }
        },
        Attributes=attributes,
    )
    result = ""
    for face in response['FaceDetails']:
        result += "  Face {Confidence}%\n".format(**face)
        result += "  Age : {Low} to {High} years\n".format(**face['AgeRange'])
        # emotions
        for emotion in face['Emotions']:
            result += "  {Type} : {Confidence}%\n".format(**emotion)
        # quality
        for quality, value in face['Quality'].items():
            result += "  {quality} : {value}\n".format(quality=quality, value=value)
        # facial features
        for feature, data in face.items():
            if feature not in FEATURES_BLACKLIST:
                result += "  {feature}({data[Value]}) : {data[Confidence]}%\n".format(feature=feature, data=data)

    result +="\n\n"
    return result

@app.route('/result')
def result():
    return render_template('result.html')

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
        
        flash(message="Success image analized",category="success")
        return render_template('result.html',out=output)

    flash(message="An error ocurred",category="error")
    return redirect(url_for('index'))


@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])