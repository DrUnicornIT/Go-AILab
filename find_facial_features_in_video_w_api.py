import cv2
from face_util import load_encoding_images, detect_known_faces

# Encode faces from a folder
load_encoding_images("sample_images/")

# Load Camera
video = cv2.VideoCapture(0);



if video.isOpened() == False: 
    print("Error reading video file")
    
# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('./static/output1.mp4', fourcc, 10.0, size)

while True:
    ret, frame = video.read()
    # Detect Faces
    if ret == True:
        face_locations, face_names = detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.putText(frame, str(abs(x1-x2)),(x1, y1 - 35), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.putText(frame, str(abs(y1-y2)),(x1, y1 - 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        # out.write(frame)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    else : 
        break

video.release()
out.release()
cv2.destroyAllWindows()
print("Video finished.")