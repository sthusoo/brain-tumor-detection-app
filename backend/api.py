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
ML_MODEL_FILENAME = 'trained_model.h5'

#Load operation system library
import os

#website libraries
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

#Load math library
import numpy as np

#Load machine learning libraries
from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import torch
import torch.nn.functional as F
import tensorflow.compat.v1 as tf1
tf1.disable_v2_behavior()

import tensorflow as tf
from tensorflow import keras
from keras import backend as K

from PIL import Image
import requests
import re
from io import BytesIO
from urllib.request import urlretrieve
import base64

# create website object
app = Flask(__name__)
CORS(app)
app.config['SECRET KEY'] = 'a secret key'
app.secret_key = 'super secret key'


def load_model_from_file():
    #Set up the machine learning session
    mySession = tf1.Session()
    set_session(mySession)
    myModel = load_model(ML_MODEL_FILENAME)
    myGraph = tf1.get_default_graph()
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
    if request.method == 'GET':
        return jsonify({"method": request.method, "status": "200"})
    else: # if request.method == 'POST'
        image_url = find_image_url(request.data.decode('utf-8'))
        return redirect(url_for('uploaded_file', URL=image_url[0]))
        
@app.route('/predict')
def uploaded_file():
    urlretrieve(request.args.get('URL'), "uploaded_image.png")

    img = keras.preprocessing.image.load_img("uploaded_image.png", target_size=(180,180))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    mySession = app.config['SESSION']
    myModel = app.config['MODEL']
    myGraph = app.config['GRAPH']

    model = keras.models.load_model(ML_MODEL_FILENAME)
    predictions = model.predict(img_array, steps=1) # array
    pred = torch.from_numpy(predictions[0]) # Tensor
    score_number = F.softmax(pred, dim=0).numpy() # array
    max_score = np.max(score_number) # number

    confidence_percent = round(max_score * 100, 2)

    class_names = ['Normal', 'Tumor']

    classification = class_names[np.argmax(score_number)]
    
    response = {
    "method": "POST",
    "status": 200, 
    "predictions": str(predictions[0]), 
    "confidence": confidence_percent,
    "classification": classification, 
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