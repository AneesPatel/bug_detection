from flask import Blueprint, render_template, request
from inference import predict_bug_species

# Create a blueprint named 'predict'
predict = Blueprint('predict', __name__)

# Define a route '/predict' within the blueprint to handle POST requests
@predict.route('/predict', methods=['POST'])
def predict_route():
    if request.method == 'POST':
        # Check if the image file is present in the request
        if 'image' not in request.files:
            return render_template('error.html', message='No image uploaded')

        # Retrieve the image file from the request
        image = request.files['image']

        # Call the predict_bug_species function to perform inference
        predicted_species, confidence = predict_bug_species(image)

        # Render the result template with the predicted species and confidence
        return render_template('result.html', species=predicted_species, confidence=confidence)
