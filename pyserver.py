from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import zipfile
import webbrowser

def create_app(file_path):
    app = Flask(__name__)
    CORS(app)

    @app.route('/get_geogebra_json', methods=['POST'])
    def get_geogebra_json():
        mdata = request.get_json()
        json_data = mdata.get("archive")
        json_data = json.loads(json.dumps(json_data, indent=4))
        for single_geobebra_file in json_data:
            os.makedirs("temp", exist_ok=True)
            with open(f"temp/{single_geobebra_file['fileName']}", 'w', encoding='utf-8') as ggb_file:
                ggb_file.write(single_geobebra_file["fileContent"].replace("\\n", "\n"))
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        os.makedirs(directory, exist_ok=True)

        try:
            with zipfile.ZipFile(file_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
                for root, _, files in os.walk("temp"):
                    for file in files:
                        file_path_to_zip = os.path.join(root, file)
                        arcname = os.path.relpath(file_path_to_zip, "temp")
                        zipf.write(file_path_to_zip, arcname=arcname)
            return jsonify({'status': 'success', 'message': "all right"})
        except Exception as e:
            return jsonify({'status': 'error', 'message': f"Error creating zip: {str(e)}"})
    return app


if __name__ == '__main__':
    app = create_app("saved_file/meow.ggb") 
    @app.route('/')
    def index():    
        initial_command = r'api.evalCommand("M=(2,0)\nE=(1,3)\nO=(0,0)\na = Angle(M,E,O)");'
        return render_template('main.html', initial_command=initial_command)
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    