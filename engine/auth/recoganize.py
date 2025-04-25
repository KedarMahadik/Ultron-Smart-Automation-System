# import cv2
# import face_recognition
# import numpy as np
# import os

# class AuthenticateFace:
#     def __init__(self):
#         self.user_image_path = "engine/auth/user.jpg"  # Path to stored user face image

#     def authenticate_face_with_camera(self):
#         print("[INFO] Starting Face Authentication...")

#         if not os.path.exists(self.user_image_path):
#             print("[ERROR] User image not found. Please register your face first.")
#             return 0  # Authentication failed

#         # Load stored user image
#         user_image = face_recognition.load_image_file(self.user_image_path)
#         user_encoding = face_recognition.face_encodings(user_image)[0]

#         # Start webcam
#         cap = cv2.VideoCapture(0)

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("[ERROR] Failed to capture image.")
#                 break

#             # Convert frame to RGB (required by face_recognition)
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Detect faces
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             for face_encoding in face_encodings:
#                 # Compare captured face with stored face
#                 matches = face_recognition.compare_faces([user_encoding], face_encoding)
#                 if True in matches:
#                     print("[SUCCESS] Face Authentication Successful!")
#                     cap.release()
#                     cv2.destroyAllWindows()
#                     return 1  # Authentication successful

#             # Display video feed
#             cv2.imshow("Face Authentication", frame)

#             # Press 'Q' to exit
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cap.release()
#         cv2.destroyAllWindows()
#         print("[FAILED] Face Authentication Failed.")
#         return 0  # Authentication failed


# ------------------------------------------------- new code ---------------------------------------------

from sys import flags
import time
import cv2
import pyautogui as p


def AuthenticateFace():

    flag = ""
    # Local Binary Patterns Histograms
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read('engine\\auth\\trainer\\trainer.yml')  # load trained model
    cascadePath = "engine\\auth\\haarcascade_frontalface_default.xml"
    # initializing haar cascade for object detection approach
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type


    id = 2  # number of persons you want to Recognize


    names = ['', 'Kedar']  # names, leave first empty bcz counter starts from 0


    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)  # set video FrameWidht
    cam.set(4, 480)  # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    # flag = True

    while True:

        ret, img = cam.read()  # read the frames using the above created object

        # The function converts an input image from one color space to another
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for(x, y, w, h) in faces:

            # used to draw a rectangle on any image
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # to predict on every single image
            id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])

            # Check if accuracy is less them 100 ==> "0" is perfect match
            if (accuracy < 100):
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 1
            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 0

            cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x+5, y+h-5),
                        font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        if flag == 1:
            break
            

    # Do a bit of cleanup
    
    cam.release()
    cv2.destroyAllWindows()
    return flag
