from flask import Flask, render_template, request
from flask_cors import CORS
import json
import os
import zipfile


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    initial_command = r"MEOW = (0,1)\nKWA = (1,3)"     #Команды которые будут исполнены
    return render_template('test.html', initial_command=initial_command)  

from flask import request

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/get_geogebra_json', methods=['POST'])
def get_geogebra_json():
    mdata = request.get_json()
    json_data = mdata.get("archive")  
    json_data = json.loads(json.dumps(json_data, indent=4))
    for single_geobebra_file in json_data:
        with open(f"ggb/{single_geobebra_file["fileName"]}", 'w', encoding='utf-8') as ggb_file:
            ggb_file.write(single_geobebra_file["fileContent"].replace("\\n", "\n"))
    with zipfile.ZipFile("GeoGebra_file.ggb", 'w', compression=zipfile.ZIP_STORED) as zipf:  
        for root, _, files in os.walk("ggb"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "ggb") 
                zipf.write(file_path, arcname=arcname)
    shutdown_server()
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    