from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

MODEL_PATH = 'model/model.h5'

model = load_model(MODEL_PATH)
app = Flask(__name__)

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size = (200, 200))
    x = image.img_to_array(img)
    x = x / 255
    x = np.expand_dims(x, axis = 0)
    preds = model.predict(x)
    actual_prediction = np.argmax(preds) + 1
    return actual_prediction

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
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None

if __name__ == '__main__':
    app.run(debug=True)
