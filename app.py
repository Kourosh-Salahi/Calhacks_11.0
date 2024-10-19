from flask import Flask, Response, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import cv2
import mediapipe as mp

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire Flask app

# Initialize Mediapipe modules
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Create a holistic model instance
holistic_model = mp_holistic.Holistic()

capture = cv2.VideoCapture(0)

# Global variable to track whether all landmarks are visible
inframe = False

def generate_frames_with_landmarks():
    global inframe
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (400, 300))

            # Convert the frame from BGR to RGB (required by Mediapipe)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with Mediapipe
            image.flags.writeable = False  # To improve performance
            results = holistic_model.process(image)
            image.flags.writeable = True

            # Convert back to BGR for OpenCV rendering
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Assume not all landmarks are in frame initially
            inframe = False

            # Check if face landmarks are present
            if results.face_landmarks:
                inframe = True
                mp_drawing.draw_landmarks(
                    image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
                )
            else:
                inframe = False  # If no face landmarks, set inframe to False

            # Check if right hand landmarks are present
            if results.right_hand_landmarks:
                inframe = inframe and True  # Keep True only if previous landmarks also detected
                mp_drawing.draw_landmarks(
                    image,
                    results.right_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS
                )
            else:
                inframe = False  # If no right hand landmarks, set inframe to False

            # Check if left hand landmarks are present
            if results.left_hand_landmarks:
                inframe = inframe and True  # Keep True only if previous landmarks also detected
                mp_drawing.draw_landmarks(
                    image,
                    results.left_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS
                )
            else:
                inframe = False  # If no left hand landmarks, set inframe to False

            # Encode the processed frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # Yield the frame in a byte format and stream inframe value
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames_without_landmarks(): 
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (400, 300))

            # Encode the raw frame in JPEG format (no landmark processing)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in a byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed_with_landmarks():
    # Video streaming route with landmarks
    return Response(generate_frames_with_landmarks(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_no_landmarks')
def video_feed_without_landmarks():
    # Video streaming route without landmarks
    return Response(generate_frames_without_landmarks(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/inframe_status')
def inframe_status():
    # API endpoint to return the inframe status
    return jsonify({"inframe": inframe})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
