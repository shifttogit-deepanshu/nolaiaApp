from __future__ import division, print_function
# coding=utf-8

import numpy as np
import os
import cv2
import tensorflow.keras as keras
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='malaria.h5'

# Load your trained model
model = load_model(MODEL_PATH)


def load(filename):
    with tf.device('/cpu:0'):
        img = cv2.imread(filename)
        plt.imshow(img)
        img = image.load_img(filename, target_size = (64, 64))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis = 0)
        index = model.predict(img)
        index = index.argmax().item()
        if index == 0:
            return "Parasitic"
        elif index == 1:
            return "Non-Parasitic"
        else :
            return "No response"


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="The Person is Infected With Malaria"
    else:
        preds="The Person is not Infected With Malaria"
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = load(file_path)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0")