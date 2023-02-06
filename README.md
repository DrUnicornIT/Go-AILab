# Go-AILab
Demo project - python
- https://github.com/DrUnicornIT/Go-AILab

- Source
    - Github: https://github.com/ageitgey/face_recognition
    - Travis: https://travis-ci.org/github/ageitgey/face_recognition


## Installation
  ```sh
    pip install --save face_recognition
    pip install opencv-python
  ```
### Requirements

  * Python 4+ or Python 3.7
  * macOS or Linux (Windows not officially supported, but might work)

#### `face_detection` command line tool

The `face_detection` command lets you find the location (pixel coordinatates) 
of any faces in an image.

Just run the command `face_detection`, passing in a folder of images 
to check (or a single image):

```sh
  python flask_server_v1.py 
  python demo_client.py
```

It prints one line for each face that was detected. The coordinates
reported are the top, right, bottom and left coordinates of the face (in pixels).