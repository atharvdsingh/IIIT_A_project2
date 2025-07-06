from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import uuid

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

    try:
        decision_paths = viz(file_path)

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

# Keep the original endpoint for backward compatibility
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
