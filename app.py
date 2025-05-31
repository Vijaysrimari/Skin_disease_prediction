from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Disease classes
CLASSES = ['Healthy', 'Acne', 'Eczema', 'Melanoma', 'Psoriasis']

def predict_image(file_path):
    # For demo purposes, return random probabilities
    return np.random.random(len(CLASSES))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file:
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get predictions
            predictions = predict_image(filepath)
            
            # Create results
            results = [{'class': class_name, 'probability': float(prob)} 
                      for class_name, prob in zip(CLASSES, predictions)]
            
            # Sort by probability
            results.sort(key=lambda x: x['probability'], reverse=True)
            
            # Clean up the uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({'predictions': results})
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'})

if __name__ == '__main__':
    print("Server starting... Please wait...")
    print("Once started, open your web browser and go to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000) 