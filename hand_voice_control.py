#hand_voice_control.py
import cv2

import mediapipe as mp
import pyautogui
import speech_recognition as sr
import time
import os  # ✅ missing import
from pynput.mouse import Button, Controller

# Initialize Modules
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils
recognizer = sr.Recognizer()
mouse = Controller()

# Capture Video Feed
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Cursor Movement Correction (Flipping X-Axis)
def map_coordinates(x, y, frame_width, frame_height):
    mapped_x = int(screen_width - (x / frame_width) * screen_width)  # Flip X
    mapped_y = int((y / frame_height) * screen_height)
    return mapped_x, mapped_y

# Recognize Gestures and Actions
def recognize_gesture(hand_landmarks, frame):
    frame_height, frame_width, _ = frame.shape
    landmarks = [(int(lm.x * frame_width), int(lm.y * frame_height)) for lm in hand_landmarks.landmark]

    index_finger = landmarks[8]
    thumb = landmarks[4]

    # Move Mouse Cursor
    mouse_x, mouse_y = map_coordinates(index_finger[0], index_finger[1], frame_width, frame_height)
    pyautogui.moveTo(mouse_x, mouse_y, duration=0.1)

    # Left Click Gesture
    if abs(index_finger[0] - thumb[0]) < 30 and abs(index_finger[1] - thumb[1]) < 30:
        pyautogui.click()
        print("🖱️ Left Click")

# Voice Commands
def recognize_voice():
    with sr.Microphone() as source:
        print("🎤 Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

            command = recognizer.recognize_google(audio).lower()
            print(f"🔊 You said: {command}")

            if "search topic" in command:
                os.system("streamlit run frontend.py")
            elif "highlight text" in command:
                pyautogui.hotkey("ctrl", "a")
            elif "volume up" in command:
                pyautogui.press("volumeup")
            elif "volume down" in command:
                pyautogui.press("volumedown")

        except sr.WaitTimeoutError:
            print("⌛ No speech detected in time. Skipping.")
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.RequestError:
            print("❌ Speech recognition service is down.")


# Main Loop
last_voice_time = 0  # Timestamp for voice delay

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            recognize_gesture(hand_landmarks, frame)

    cv2.imshow("🖐️ Hand + 🎤 Voice Control", frame)

    # Voice every 10 seconds (clean and efficient)
    if time.time() - last_voice_time > 10:
        recognize_voice()
        last_voice_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
