import os
import sys

from flask import Flask, request, send_from_directory
from flask_cors import CORS

PROFILE_IMAGE_FILE_PATH= os.getcwd() + "/woojoo/assets/image/profile"

app = Flask(__name__)
base_dir = os.getcwd()
sys.path.append(base_dir)
app.config.from_pyfile(f"{base_dir}/woojoo/default.cfg")
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
CORS(app, supports_credentials=True)


@app.route('/cdn/profile/image/<image_name>', methods=["GET"])
def get_profile_image(image_name):
    return send_from_directory(
        PROFILE_IMAGE_FILE_PATH, 
        image_name
    )


@app.route('/cdn/image', methods=["POST"])
def upload():
    file = request.files.get('file')
    full_path = os.path.join(PROFILE_IMAGE_FILE_PATH, file.filename)
    file.save(full_path)
    return 'success'

    
@app.route('/cdn/image', methods=["DELETE"])
def delete():
    profile_image_name = request.get_json()['filename']
    try:
        full_path = os.path.join(PROFILE_IMAGE_FILE_PATH, profile_image_name)
        os.remove(full_path)
    except:
        pass
    return 'success'