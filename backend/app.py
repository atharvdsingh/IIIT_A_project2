from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import os
import sys
import asyncio
import json
import uuid  # to create unique filenames


from model.backendModel import viz


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    if file_path:
        try:
            decision_paths = viz(file_path)

            json_path = os.path.join("folder", "decision_paths.json")
            with open(json_path, "w") as f:
                json.dump(decision_paths, f, indent=2)

            # Return it as a file for download
            return send_file(json_path, as_attachment=True)
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    return jsonify({'successtouch file/__init__.py': 'File uploaded successfully', 'path': file_path}), 200
    

if __name__ == "__main__":
    app.run(debug=True)
