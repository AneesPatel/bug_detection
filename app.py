from flask import Flask, render_template, request
from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np

app = Flask(__name__)

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="##########"
)

@app.route('/')
def index():
    return render_template('index.html')

def predict_bug_species(image):
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0

    result = CLIENT.infer(img, model_id="insect_detect_classification_v2/1")

    predicted_class = result['predicted_class']
    confidence = result['confidence']

    return predicted_class, confidence

@app.route('/predict', methods=['POST'])

def predict():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('error.html', message='No image uploaded')
        image = request.files['image']
        predicted_species, confidence = predict_bug_species(image)

        if 'predicted_class' not in predicted_species:
            return render_template('error.html', message='Predicted class not found in result')

        return render_template('result.html', species=predicted_species['predicted_class'], confidence=confidence)


if __name__ == '__main__':
    app.run(debug=True)
