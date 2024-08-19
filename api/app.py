#dont need this for now directly run -> python3 model.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS         
from chat import get_response 

app = Flask(__name__)
CORS(app)  #for cross origin request




@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    
    #error handling needs to be done -> check text is valid or not
    
    response = get_response(text)
    
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True) #for testing
