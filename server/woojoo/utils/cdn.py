import os
import requests
from io import BufferedReader
from werkzeug.datastructures import FileStorage
import time

class CDN():
    def __init__(self):
        self.cdn_url = 'http://127.0.0.1:4000'
            
    def _send_image(self, filename, image, content_type):
        res = requests.post(
            f'{self.cdn_url}/cdn/image',
            files={"file": (filename, image, content_type)},
        )
        return res.status_code
    
    def _delete_file(self, filename):
        res = requests.delete(
            f'{self.cdn_url}/cdn/image',
            json={"filename":filename}
        )
        return res.status_code

    def send_stream_image_file(self, file: FileStorage):
        image = BufferedReader(file)
        
        root, ext = os.path.splitext(file.filename)
        now_time = int(time.time())
        filename = f"profile_{now_time}{ext}"

        status_code = self._send_image(filename=filename, image=image, content_type=file.content_type)
        if status_code == 200:
            return filename
        else:
            return status_code

        
    def delete_file(self, filename):
        status_code = self._delete_file(filename)
        if status_code == 200:
            return filename
        else:
            return status_code