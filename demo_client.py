from joblib import parallel_backend
import requests
import json
import base64
## import ipdb

def test_face_match():
    url = 'http://127.0.0.1:5001/face_match'
    # open file in binary mode
    files = {'file1': open('sample_images/Obama1.jpg', 'rb'),
             'file2': open('sample_images/Obama2.jpg', 'rb')}     
    resp = requests.post(url, files=files)
    print( 'face_match response:\n', json.dumps(resp.json()) )
    
def test_face_rec():
    url = 'http://127.0.0.1:5001/face_rec'
    # open file in binary mode
    params = {'facial_features': 'true', 'face_locations':'true'}
    files = {'file': open('sample_images/CongNguyen.jpg', 'rb')} 
    resp = requests.post(url, files = files, params=params)
    f = open("face_res.JSON", "w")
    print( json.dumps(resp.json(),indent=2), file=f)
    f.close()

def test_face_rec_json():
    url = 'http://127.0.0.1:5001/face_rec'
    # encode image as base64 text string.
    # Note: Must convert output bytes string from b64encode to an ascii string to form a JSON, e.g. b'abc' to 'abc'.
    with open('sample_images/obama2.jpg', 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('ascii')
        
    data = {'file_format':'jpg', 'image_data': image_data}
    f = open("ascii.JSON", "a")
    
    print(json.dumps(data,indent=2), file=f)
    f.close()
    
    params = {'facial_features': 'true', 'face_locations':'true'}
    resp = requests.post(url, json = data, params = params)
    print( 'face_rec response:\n', json.dumps(resp.json()) )

def test_add_image(): 
    url = 'http://127.0.0.1:5001/face_add'
    # open file in binary mode
    params = {'name': 'ABCDEFGH',}
    files = {'file': open('sample_images/CongNguyen.jpg', 'rb')} 
    resp = requests.post(url, params=params, files = files)
    
    with open("addImage.JSON","r+") as file :
        file_data = json.load(file)
        file_data["members"].append(resp.json())
        file.seek(0)
        json.dump(file_data, file,indent=4)
    print( 'test_add response:\n', json.dumps(resp.json()) )


def detect_faces():
    url = 'http://127.0.0.1:5001/detect_faces'
    # open file in binary mode
    files = {'file': open('sample_videos/abctest1.mp4', 'rb')} 
    resp = requests.post(url, files = files)
    print( 'dectect_faces response:\n', json.dumps(resp.json()) )
    
def main():
    test_face_match()
    test_face_rec()
    test_face_rec_json()
    test_add_image()
    detect_faces()
    
if __name__ == '__main__':
    main()