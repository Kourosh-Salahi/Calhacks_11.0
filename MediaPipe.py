import cv2
import time
import mediapipe as mp

# Grabbing the Holistic Model from Mediapipe and
# Initializing the Model
mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
 
# Initializing the drawing utils for drawing the facial landmarks on image
mp_drawing = mp.solutions.drawing_utils

#WORKING for Groq
import cv2
import mediapipe as mp
import re
from groq import Groq
import time

# Initialize MediaPipe components
mp_holistic = mp.solutions.holistic

# Create a holistic model instance
holistic_model = mp_holistic.Holistic()

# Video capture from the default camera
capture = cv2.VideoCapture(0)

# Define frame-skip rate (e.g., process 1 out of every 'n' frames)
frame_skip = 2
frame_count = 0

# Initialize API client
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Variable to store ASL letters
result = ""

while capture.isOpened():
    ret, frame = capture.read()

    if not ret:
        break

    # Increment the frame count
    frame_count += 1

    # Skip frames based on the defined frame_skip rate
    if frame_count % frame_skip != 0:
        continue

    # Converting the frame from BGR to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Making predictions using holistic model
    image.flags.writeable = False
    results = holistic_model.process(image)
    image.flags.writeable = True

    hand_joints = []

    # Extracting right hand landmarks if available
    if results.right_hand_landmarks:
        right_hand_joints = [
            (id, lm.x, lm.y, lm.z)
            for id, lm in enumerate(results.right_hand_landmarks.landmark)
        ]
        hand_joints.append(right_hand_joints)

    # Extracting left hand landmarks if available
    if results.left_hand_landmarks:
        left_hand_joints = [
            (id, lm.x, lm.y, lm.z)
            for id, lm in enumerate(results.left_hand_landmarks.landmark)
        ]
        hand_joints.append(left_hand_joints)

    # Prepare content for the API request
    if hand_joints:
        content = (
            f"{hand_joints} Each of these points is a number followed by a 3D vector "
            f"(number, x, y, z), each of the numbers corresponds to a joint on the hand. "
            f"0. WRIST 1. THUMB_CMC 2. THUMB_MCP 3. THUMB_IP 4. THUMB_TIP "
            f"5. INDEX_FINGER_MCP 6. INDEX_FINGER_PIP 7. INDEX_FINGER_DIP 8. INDEX_FINGER_TIP "
            f"9. MIDDLE_FINGER_MCP 10. MIDDLE_FINGER_PIP 11. MIDDLE_FINGER_DIP 12. MIDDLE_FINGER_TIP "
            f"13. RING_FINGER_MCP 14. RING_FINGER_PIP 15. RING_FINGER_DIP 16. RING_FINGER_TIP "
            f"17. PINKY_MCP 18. PINKY_PIP 19. PINKY_DIP 20. PINKY_TIP. "
            f"What ASL letter does this create? Please return the answer in the format 'ASL Letter: 'X''."
        )

        try:
            completion = client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[{"role": "user", "content": content}],
                temperature=0.5,
                max_tokens=500,
                top_p=1,
                stream=False,
            )

            text = completion.choices[0].message.content
            #print(text)

            # Extract ASL letter from the API response
            # ASL_letter_match = re.search(r'ASL Letter: ["\']([A-Z])["\']', text)
            # if ASL_letter_match:
            #     asl_letter = ASL_letter_match.group(1)
            #     result += asl_letter
            #     print(result)  # Print the updated result

            ASL_letter_match = re.search(r'ASL Letter:\s*["\']?([A-Z])["\']?', text)

            if ASL_letter_match:
                asl_letter = ASL_letter_match.group(1)
                result += asl_letter
                print(result)
            else:
                print("No ASL letter found in the response.")

        except Exception as e:
            print(f"Error with API response: {e}")

    time.sleep(2)

    # Enter key 'q' to break the loop
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
capture.release()
cv2.destroyAllWindows()