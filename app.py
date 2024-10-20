from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import mediapipe as mp
import time
import os
import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamFace

app = Flask(__name__)
CORS(app)

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic_model = mp_holistic.Holistic()

capture = cv2.VideoCapture(0)

inframe = False
sentiment_result = ""  # Global variable to store the latest sentiment result


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


async def analyze_sentiment():
    global sentiment_result
    ANALYSIS_INTERVAL = 2
    temp_image_path = os.path.join(os.getcwd(), 'temp.jpg')

    last_analysis_time = 0  # Track when the last analysis happened
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (400, 300))
            ret, buffer = cv2.imencode('.jpg', frame)

            # Save the buffer as 'temp.jpg' in the current directory
            try:
                with open(temp_image_path, 'wb') as f:
                    f.write(buffer)
                print(f"Image saved to {temp_image_path}")

            except Exception as e:
                print(f"Error writing temp.jpg: {e}")

            # Check if 2 seconds have passed since the last analysis
            current_time = time.time()
            if current_time - last_analysis_time > ANALYSIS_INTERVAL:
                # Perform sentiment analysis only every 2 seconds
                last_analysis_time = current_time

                # Perform sentiment analysis on the image
                client = AsyncHumeClient(api_key="8I63Z7n9vDCcq2GgpEqjABPO5LvoHONQc2NPQFRT60ZQpMvv")

                model_config = Config(face=StreamFace())
                stream_options = StreamConnectOptions(config=model_config)

                async with client.expression_measurement.stream.connect(options=stream_options) as socket:
                    result = await socket.send_file(temp_image_path)



                    # Access the predictions safely
                    if result.face and result.face.predictions:
                        first_prediction = result.face.predictions[0]  # Get the first prediction
                        if first_prediction.emotions:
                            # Extracting the top emotion based on its score
                            top_emotion = max(first_prediction.emotions, key=lambda e: e.score)
                            sentiment_result = top_emotion.name  # Store the top emotion name
                            print(f"Top emotion detected: {top_emotion.name}")
                        else:
                            print("No emotions detected.")
                            sentiment_result = "No emotions detected"
                    else:
                        print("No face or predictions detected.")
                        sentiment_result = "No face or predictions detected"
                
            return sentiment_result


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


@app.route('/sentiment')
async def sentiment():
    print("Sentiment route hit")
    sentiment_result = await analyze_sentiment()  # Ensure the sentiment analysis is awaited
    return jsonify({"sentiment": sentiment_result})


if __name__ == "__main__":
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, load_dotenv=False)
