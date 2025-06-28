import mediapipe as mp
import cv2


camera = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

with mp_pose.Pose(static_image_mode = True) as pose:
    with mp_hands.Hands() as hands:
        while camera.isOpened():
            ret, img = camera.read()
            img2 = img.copy()

            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            results = hands.process(img2)
            img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)

            result = pose.process(img)

            red_dot = mp_draw.DrawingSpec(color = (0,0,255), thickness = -1, circle_radius = 1)
            mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            handRaised = False
            if result.pose_landmarks:
                if result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y>result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y or result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y>result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y:
                    cv2.putText(img, "Hand is Raised", (50, 50), 0, 2, 255)
                    handRaised = True
            cv2.imshow('Pose Marked', img)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img2, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
                    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y<hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y<hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y<hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y>hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y>hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y and handRaised:
                        cv2.putText(img2, "We Have a Volunteer as Tribute", (50, 50), 0, 1, 255)
            cv2.imshow('Hands Marked', img2)

            """if result.pose_landmarks:
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
                        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y:
                            cv2.putText(img, "We Have a Volunteer as Tribute", (50, 50), 0, 1, 255)
                        elif result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y > result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y or result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y > result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y:
                            cv2.putText(img, "Hand is Raised", (50, 50), 0, 2, 255)
            """



            key = cv2.waitKey(1)
            if key == 27:
                break
                camera.release()
                cv2.destroyAllWindows()
        else:
            print("Camera not found")