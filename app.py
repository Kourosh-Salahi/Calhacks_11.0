from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

# Initialize Mediapipe modules
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Create a holistic model instance
holistic_model = mp_holistic.Holistic()

capture = cv2.VideoCapture(0)

def generate_frames_with_landmarks():
  # Use the default camera

    while True:
        # Capture frame by frame
        success, frame = capture.read()
        if not success:
            break
        else:
            # Resizing the frame for better view
            frame = cv2.resize(frame, (400, 300))

            # Convert the frame from BGR to RGB (required by Mediapipe)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with Mediapipe
            image.flags.writeable = False  # To improve performance
            results = holistic_model.process(image)
            image.flags.writeable = True

            # Convert back to BGR for OpenCV rendering
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.face_landmarks:
                mp_drawing.draw_landmarks(
                    image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
                )

            # Draw right hand landmarks
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Draw left hand landmarks
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Encode the processed frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # Yield the frame in a byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames_without_landmarks(): 
    while True:
        # Capture frame by frame
        success, frame = capture.read()
        if not success:
            break
        else:
            # Resizing the frame for better view
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
