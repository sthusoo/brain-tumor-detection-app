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
from werkzeug.utils import secure_filename

#Load math library
import numpy as np

#Load machine learning libraries
from tensorflow.keras.preprocessing import image
from keras.models import load_model
# from keras.backend import set_session
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# create website object
app = Flask(__name__)


def load_model_from_file():
    #Set up the machine learning session
    mySession = tf.Session()
    tf.compat.v1.keras.backend.set_session(mySession)
    myModel = load_model(ML_MODEL_FILENAME)
    myGraph = tf.get_default_graph()
    return (mySession,myModel,myGraph)

# makes sure file is not malicious
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# define view for top level page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # initial webpage load
    if request.method == 'GET':
        return render_template('index.html',myX=X,myY=Y,mySampleX=sampleX,mySampleY=sampleY,len=len(results),results=results)
    else: # if request.method == 'POST'
        # check if post request has file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if it isn't an image file
        if not allowed_file(file.filename):
            flash('I only accept files of type ' + str(ALLOWED_EXTENSIONS))
            return redirect(request.url)
        # when user uploads file with good parameters
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        
@app.route('/predict/<filename>')
def uploaded_file(filename):
    test_img = image.load_img(UPLOAD_FOLDER+'/'+filename, target_size=(150,150))
    test_img = image.img_to_array(test_img)
    test_img = np.expand_dims(test_img, axis=0)
    
    mySession = app.config['SESSION']
    myModel = app.config['MODEL']
    myGraph = app.config['GRAPH']
    
    with myGraph.as_default():
        tf.compat.v1.keras.backend.set_session(mySession)
        prediction = myModel.predict(test_img)
        # score = tf.nn.softmax(prediciton[0])
        image_src = '/'+UPLOAD_FOLDER+'/'+filename
        if prediction[0][0] > 0.5:
            classification = Y # Tumor
        else:
            classification = X # Normal
        response = {
        "status": 200, 
        "prediction": prediction[0][0], 
        "classification": classification, 
        "imagePath": image_src
        }

        return jsonify(response)


if __name__ == "__main__":
    (mySession, myModel, myGraph) = load_model_from_file()
    
    app.config['SECRET KEY'] = 'a secret key'
    
    app.config['SESSION'] = mySession
    app.config['MODEL'] = myModel
    app.config['GRAPH'] = myGraph
    
    app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB upload limit
    
    app.run()