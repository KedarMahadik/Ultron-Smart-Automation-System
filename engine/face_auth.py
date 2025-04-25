import cv2
import face_recognition
import numpy as np

def authenticate_face_with_camera():
    known_face_encodings = []
    known_face_names = ["User"]  # Change "User" to your name

    # Load a sample picture and learn how to recognize it
    try:
        user_image = face_recognition.load_image_file("face_auth/user.jpg")  # Ensure you have this image
        user_face_encoding = face_recognition.face_encodings(user_image)[0]
        known_face_encodings.append(user_face_encoding)
    except IndexError:
        print("ERROR: No face found in user image!")
        return 0

    # Initialize Webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Optimize for speed
        rgb_small_frame = small_frame[:, :, ::-1]  # Convert BGR to RGB

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                video_capture.release()
                cv2.destroyAllWindows()
                return 1  # Authentication successful

        cv2.imshow("Face Authentication", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return 0  # Authentication failed
