from crypt import methods
from flask import Flask, render_template, request, redirect, render_template
from werkzeug.utils import secure_filename
import os
import json
from face_util import compare_faces, face_rec, find_facial_features, find_face_locations, load_encoding_images,detect_known_faces
import re
import base64
import cv2
import matplotlib



app = Flask(__name__, template_folder='./template', static_folder = './static')

UPLOAD_FOLDER = 'received_files'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'mp4']

load_encoding_images("sample_images/")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    if request.is_json:
        json_data = request.get_json(cache=True)
        # replace image_data with '<image base64 data>'
        if json_data.get('image_data', None) is not None:
            json_data['image_data'] = '<image base64 data>'
        else: 
            print('request image_data is None.')
        print(json.dumps(json_data,indent=4))
    else: # form data
        body_data=request.get_data()
        # replace image raw data with string '<image raw data>'
        body_sub_image_data=re.sub(b'(\r\n\r\n)(.*?)(\r\n--)',br'\1<image raw data>\3', body_data,flags=re.DOTALL)
        print(body_sub_image_data.decode('utf-8'))
    # print(body_data[0:500] + b'...' + body_data[-500:]) # raw binary

@app.route('/face_add', methods=['POST', 'GET'])
def face_add_image(): 
    if request.method == 'POST':
        # Print request url, headers and content
        print_request(request)
        # JSON data format
        if request.is_json:
            """ Sample data
            {'file_format':'jpg', 'image_data': <base64 ascii string>}
            """
            json_data = request.get_json(cache=False)
            file_format = json_data.get('file_format', None)
            image_data = json_data.get('image_data', None)
            if file_format not in ALLOWED_EXTENSIONS or image_data is None:
                return '{"error":"Invalid JSON."}'

            file = os.path.join(UPLOAD_FOLDER, 'image.' + file_format)
            with open(file,'wb') as f:
                # Note: Convert ascii string to bytes string first, e.g. 'abc' to b'abc', before decode as a base64 string.
                f.write(base64.b64decode(image_data.encode('ascii'))) 
        
        # form data format
        else: 
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            if 'name' not in request.args:
                print('No name part')
                return redirect(request.url)
            
            file = request.files.get('file')
            name = request.args.get('name')
            # if user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            with open("addImage.JSON", "r+") as cur_file :
                file_data = json.load(cur_file)
                for item in file_data['members']:
                    if item['name'] == name:
                        print('We have this name already')
                        return redirect(request.url)
                     
            if not allowed_file(file.filename):
                return '{"error":"Invalid image file format."}'
        resp_data = {"name": name}
        
        # Process image file
        # Note file could be a filename or a file object.
        path = "./sample_images/" + name + "." + file.filename.rsplit('.', 1)[1].lower()
        resp_data.update({"path": path})
        with open(path, 'wb') as f:
            f.write(file.read())
        # get parameters from url if any.
        # facial_features parameter:
        print(resp_data)
        return json.dumps(resp_data)

    return render_template('face_add.html')

@app.route('/face_rec', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
        # Print request url, headers and content
        print_request(request)
        # JSON data format
        if request.is_json:
            """ Sample data
            {'file_format':'jpg', 'image_data': <base64 ascii string>}
            """
            json_data = request.get_json(cache=False)
            file_format = json_data.get('file_format', None)
            image_data = json_data.get('image_data', None)
            if file_format not in ALLOWED_EXTENSIONS or image_data is None:
                return '{"error":"Invalid JSON."}'

            file = os.path.join(UPLOAD_FOLDER, 'image.' + file_format)
            with open(file,'wb') as f:
                # Note: Convert ascii string to bytes string first, e.g. 'abc' to b'abc', before decode as a base64 string.
                f.write(base64.b64decode(image_data.encode('ascii'))) 
        
        # form data format
        else: 
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files.get('file')
            # if user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)

            if not allowed_file(file.filename):
                return '{"error":"Invalid image file format."}'
        
        # Process image file
        # Note file could be a filename or a file object.
        name = face_rec(file)
        resp_data = {'name': name}
        # get parameters from url if any.
        # facial_features parameter:
        param_features = request.args.get('facial_features', '')
        if param_features.lower() == 'true':
            facial_features = find_facial_features(file)
            resp_data.update({'facial_features': facial_features})
            # append facial_features to resp_data
        # face_location parameters
        
        param_location = request.args.get('face_locations', '')
        if param_location.lower() == 'true':
            face_locations = find_face_locations(file)
            resp_data.update({'face_locations': face_locations})
        
        return json.dumps(resp_data)

    return render_template('face_add.html')

@app.route('/face_match', methods=['POST', 'GET'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' not in request.files) or ('file2' not in request.files):
            print('No file part')
            return redirect(request.url)

        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        # if user does not select file, browser also submit an empty part without filename
        if file1.filename == '' or file2.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file1.filename) and allowed_file(file2.filename):
            #file1.save( os.path.join(UPLOAD_FOLDER, secure_filename(file1.filename)) )
            #file2.save( os.path.join(UPLOAD_FOLDER, secure_filename(file2.filename)) )
            ret = compare_faces(file1, file2)
            resp_data = {"match": bool(ret)} # convert ret (numpy._bool) to bool for json.dumps
            return json.dumps(resp_data)

    # Return a demo page for GET request
    return render_template('face_match.html')

@app.route('/detect_faces', methods=['POST', 'GET'])
def detect_faces() :
    if request.method == 'POST':
        # Print request url, headers and content
        print_request(request)
        # JSON data format
        if request.is_json:
            """ Sample data
            {'file_format':'jpg', 'image_data': <base64 ascii string>}
            """
            json_data = request.get_json(cache=False)
            file_format = json_data.get('file_format', None)
            image_data = json_data.get('image_data', None)
            if file_format not in ALLOWED_EXTENSIONS or image_data is None:
                return '{"error":"Invalid JSON."}'

            file = os.path.join(UPLOAD_FOLDER, 'image.' + file_format)
            with open(file,'wb') as f:
                # Note: Convert ascii string to bytes string first, e.g. 'abc' to b'abc', before decode as a base64 string.
                f.write(base64.b64decode(image_data.encode('ascii'))) 
        
        # form data format
        else: 
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files.get('file')
            # if user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)

            if not allowed_file(file.filename):
                return '{"error":"Invalid image file format."}'
        
        # Process video file
        with open('./sample_videos/video.mp4', 'wb') as f:
            f.write(file.read())
            
        return '{"detect_faces":"Load image done."}'
    
    return render_template('detect_faces.html')
@app.route('/')
def index():
    return render_template('index.html')

# Run in HTTP
# When debug = True, code is reloaded on the fly while saved
app.run(host='0.0.0.0', port='5001', debug=True)