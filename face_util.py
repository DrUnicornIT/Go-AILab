import face_recognition as fr
import os
import cv2
import glob
import numpy as np



def compare_faces(file1, file2):
    """
    Compare two images and return True / False for matching.
    """
    # Load the jpg files into numpy arrays
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)
    
    # Get the face encodings for each face in each image file
    # Assume there is only 1 face in each image, so get 1st face of an image.
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = fr.compare_faces([image1_encoding], image2_encoding)    
    return results[0]

# Each face is tuple of (Name,sample image)    
known_face_encodings = []
known_faces = []
# Resize frame for a faster speed
frame_resizing = 0.25
def load_encoding_images(path):
    images_path = glob.glob(os.path.join(path, "*.*"))
    print("{} encoding images found.".format(len(images_path)))

    for img_path in images_path:
        img = cv2.imread(img_path)
        # rgb_img. 
        basename = os.path.basename(img_path)
        (filename, ext) = os.path.splitext(basename)
        # Get encoding 
        try:
            img_encoding = fr.face_encodings(img)[0]
        except IndexError as e:
            print(e)
        known_face_encodings.append(img_encoding)
        face = []
        face.append(filename)
        face.append(img_path)
        known_faces.append(face)
    f = open("known_faces.txt", "w")
    print(known_faces, file=f)
    f.close()
        
def detect_known_faces(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=frame_resizing, fy=frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # rgb_img. 
        # rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(small_frame)
    face_encodings = fr.face_encodings(small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = fr.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            type_name = known_faces[best_match_index][0]
            name = type_name[:]
        face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
    face_locations = np.array(face_locations)
    face_locations = face_locations / frame_resizing
    return face_locations.astype(int), face_names


def face_rec(file):
    """
    Return name for a known face, otherwise return 'Unknown'.
    """
    for name, known_file in known_faces:
        if compare_faces(known_file,file):
            return name
    return 'Unknown' 
    
def find_facial_features(file):
    # Load the jpg file into a numpy array
    image = fr.load_image_file(file)

    # Find all facial features in all the faces in the image
    face_landmarks_list = fr.face_landmarks(image)
    
    # return facial features if there is only 1 face in the image
    if len(face_landmarks_list) != 1:
        return {}
    else:
        return face_landmarks_list[0]
        
def find_face_locations(file):
    # Load the jpg file into a numpy array
    image = fr.load_image_file(file)

    # Find all face locations for the faces in the image
    face_locations = fr.face_locations(image)
    
    # return facial features if there is only 1 face in the image
    if len(face_locations) != 1:
        return []
    else:
        return face_locations[0] 
    
 