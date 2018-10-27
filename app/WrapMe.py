import sys
import os
import json
app_dir = os.path.dirname(os.path.abspath(__file__))
configuration_dir = os.path.join(app_dir, 'configuration')
img_proc_dir = os.path.join(app_dir, 'image_processing')

if configuration_dir not in sys.path:
    sys.path.insert(0, configuration_dir)
if img_proc_dir not in sys.path:
    sys.path.insert(0, img_proc_dir)

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from image_processing import merge_images
import validate_image
from flask import Flask, render_template, url_for, flash, request, redirect, send_file, after_this_request
from werkzeug.utils import secure_filename

wrapme = Flask(__name__)

@wrapme.route('/health_check')
def health_check():
    return json.dumps({200: 'OK'})


@wrapme.route('/info')
def info():
    server_info = {'version': '0.01',
                   'result': {200: 'OK'}}
    return json.dumps(server_info)


@wrapme.route('/')
@wrapme.route('/index')
def index():
    return render_template('index.html')

@wrapme.route('/merge_images', methods=['GET','POST'])
def merge_images():
    if request.method == 'POST':
        base = request.files['base']
        overlay = request.files['overlay']

        if base and allowed_file(base.filename):
            base_filename = secure_filename(base.filename)
            base.save(os.path.join(wrapme.config['IMAGE_DIR'], base_filename))
        if overlay and allowed_file(overlay.filename):
            overlay_filename = secure_filename(overlay.filename)
            overlay.save(os.path.join(wrapme.config['IMAGE_DIR'], overlay_filename))
        print('Merging the images')
        print(overlay_filename)
        print(base_filename)
        if validate_image.has_face(base_filename):
        	merge_images(base_filename, overlay_filename, debug=True)
    else:
        return render_template('merge.html')



@wrapme.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        uploaded_files = request.files.getlist("files[]")
        for file in uploaded_files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(wrapme.config['IMAGE_DIR'], filename))
        return render_template('upload.html')
    else:
        return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in wrapme.config['ALLOWED_EXTENSIONS']

def setup():
    working_dir = os.path.dirname(os.path.abspath(__file__))
    if working_dir not in sys.path:
        sys.path.insert(0, working_dir)
    print (sys.path)
    config_file = os.path.join(working_dir, os.path.join('configuration', 'default.json'))

    with open(config_file, 'r') as config_file:
        configuration = json.load(config_file)
        host = configuration['host']
        port = configuration['port']

    allowed_extensions = {'jpeg', 'jpg', 'png'}
    upload_dir = os.path.join(working_dir, os.path.join('static', 'images'))
    log_dir = os.path.join(working_dir, os.path.join('static', 'logs'))
    log_file = os.path.join(log_dir, 'log.txt')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    wrapme.config["IMAGE_DIR"] = upload_dir
    wrapme.config["LOG_FILE"] = log_file
    wrapme.config["ALLOWED_EXTENSIONS"] = allowed_extensions
    wrapme.config["HOST"] = host
    wrapme.config["PORT"] = port


setup()

if __name__ == '__main__':
    setup()
    wrapme.run(debug=True, host=wrapme.config["HOST"], port=int(wrapme.config["PORT"]))
