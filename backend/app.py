from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import uuid
import pandas as pd

from model.backendModel import viz

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def CheckForInteger(df):
      columns=df.columns
      for i in columns:
          unique_value=df[i].dropna().unique()
          if not set(unique_value).issubset({0,1}):
              return True
      return False
    
    

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    regularization = float(request.form.get('regularization', 0.01))
    rashomon_bound_multiplier = float(request.form.get('rashomon_bound_multiplier', 0.05))

    df=pd.read_csv(file_path)
  
    if(df.isnull().values.any()):
        return jsonify({"error":'Dataset contains null values '}),402
    if(CheckForInteger(df)):
        return jsonify({'error':'data contain interger but model works on binary value[0,1]'})
    
    
    try:
        decision_paths = viz(file_path,regularization,rashomon_bound_multiplier)

        # Return JSON data directly instead of file download
        return jsonify({
            'success': True,
            'data': decision_paths,
            'filename': f"decision_paths_{uuid.uuid4().hex[:8]}.json"
        })
    
    
    except TimeoutError:
        return jsonify({'error': 'Training took too long and was stopped.'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Keeping the previous for file returning capability for file downlaod in client side 
@app.route("/upload-file", methods=['POST'])
def upload_file_download():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        decision_paths = viz(file_path)

        # Unique filename to avoid overwriting
        filename = f"decision_paths_{uuid.uuid4().hex[:8]}.json"
        json_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(json_path, "w") as f:
            json.dump(decision_paths, f, indent=2)

        return send_file(json_path, as_attachment=True)
    
    except TimeoutError:
        return jsonify({'error': 'Training took too long and was stopped.'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
