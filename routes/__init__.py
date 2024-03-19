from flask import Flask
from .predict import predict

app = Flask(__name__)

# Register the 'predict' blueprint
app.register_blueprint(predict)

if __name__ == '__main__':
    app.run(debug=True)
