# -*- coding: utf-8 -*-
"""
Created on Thu May  6 15:37:21 2021

@author: Sheen Thusoo
"""
# 2 Classes

X = 'Normal'
Y = 'Tumor'

sampleX = 'static/normal.jpeg'
sampleY = 'static/tumor.jpg'

# Where I will keep user uploads
UPLOAD_FOLDER = 'static/uploads'
# Allowed files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# Machine Learning Model Filename
ML_MODEL_FILENAME = 'savedModel.h5'

#Load operation system library
import os

#website libraries
from flask import render_template
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

#Load math library
import numpy as np

#Load machine learning libraries
from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from PIL import Image
import requests
import re
from io import BytesIO
from urllib.request import urlopen, urlretrieve
import base64

# create website object
app = Flask(__name__)
CORS(app)
app.config['SECRET KEY'] = 'a secret key'
app.secret_key = 'super secret key'


def load_model_from_file():
    #Set up the machine learning session
    mySession = tf.Session()
    set_session(mySession)
    myModel = load_model(ML_MODEL_FILENAME)
    myGraph = tf.get_default_graph()
    return (mySession,myModel,myGraph)

# makes sure file is not malicious
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_image_url(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

# define view for top level page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # initial webpage load
    print(request.method)
    if request.method == 'GET':
        return jsonify({"method": request.method, "status": "200"})
    else: # if request.method == 'POST'
        # check if post request has file part
        image_url = find_image_url(request.data.decode('utf-8'))
        # print('the request url is ' + request.data)
        # print(image_url)
        
        # r = requests.get(image_url[0], stream=True)
        # print('the image url is ' + str(image_url))
        # image_url = Image.open(io.BytesIO(r.content))

        # if 'file' not in request.files:
        #     print('file not found')
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # if user does not select file, browser submits an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if it isn't an image file
        # if not allowed_file(file.filename):
        #     flash('I only accept files of type ' + str(ALLOWED_EXTENSIONS))
        #     return redirect(request.url)
        # when user uploads file with good parameters
        # if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD FOLDER'], filename))
        return redirect(url_for('uploaded_file', URL=image_url[0]))
        
@app.route('/predict')
def uploaded_file():
    urlretrieve(request.args.get('URL'), "sample.png")
    img = Image.open("sample.png")

    test_img = image.load_img("sample.png", target_size=(150,150))
    test_img = image.img_to_array(test_img)
    test_img = np.expand_dims(test_img, axis=0)
    
    mySession = app.config['SESSION']
    myModel = app.config['MODEL']
    myGraph = app.config['GRAPH']
    
    with myGraph.as_default():
        tf.compat.v1.keras.backend.set_session(mySession)
        prediction = myModel.predict(test_img)
        if prediction[0][0] > 0.5:
            classification = Y # Tumor
        else:
            classification = X # Normal
        response = {
        "method": "POST",
        "status": 200, 
        "prediction": str(prediction[0][0]), 
        "classification": str(classification), 
        "imagePath": str(request.args.get('URL'))
        }
        return jsonify(response)


if __name__ == "__main__":

    (mySession, myModel, myGraph) = load_model_from_file()
    
    app.config['SESSION'] = mySession
    app.config['MODEL'] = myModel
    app.config['GRAPH'] = myGraph
    
    app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB upload limit
    
    app.run(debug=True)