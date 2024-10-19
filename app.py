from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import mediapipe as mp

app = Flask(__name__)
CORS(app)

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic_model = mp_holistic.Holistic()

capture = cv2.VideoCapture(0)

inframe = False

def generate_frames_with_landmarks():
    global inframe
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (400, 300))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic_model.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            inframe = False
            if results.face_landmarks:
                inframe = True
                mp_drawing.draw_landmarks(
                    image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
                )
            else:
                inframe = False
            if results.right_hand_landmarks:
                inframe = inframe and True
                mp_drawing.draw_landmarks(
                    image,
                    results.right_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS
                )
            else:
                inframe = False
            if results.left_hand_landmarks:
                inframe = inframe and True
                mp_drawing.draw_landmarks(
                    image,
                    results.left_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS
                )
            else:
                inframe = False
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames_without_landmarks(): 
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (400, 300))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed_with_landmarks():
    return Response(generate_frames_with_landmarks(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_no_landmarks')
def video_feed_without_landmarks():
    return Response(generate_frames_without_landmarks(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/inframe_status')
def inframe_status():
    return jsonify({"inframe": inframe})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
