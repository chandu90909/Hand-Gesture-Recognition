import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

tip_ids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # IMPORTANT (makes thumb logic consistent)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    total_fingers = 0

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            h, w, c = img.shape

            lm_list = []
            for lm in landmarks:
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            finger_count = 0

            # 🔥 SIMPLE + RELIABLE THUMB LOGIC
            if lm_list[4][0] > lm_list[3][0]:
                finger_count += 1

            # 🔥 Other fingers (Y-axis)
            for i in range(1, 5):
                if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
                    finger_count += 1

            total_fingers += finger_count

            # Show per hand
            cv2.putText(img, f'Hand {idx+1}: {finger_count}',
                        (10, 100 + idx * 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    # Show total
    cv2.putText(img, f'Total: {total_fingers}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)

    cv2.imshow("Finger Counting (Stable)", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()



# import cv2
# import mediapipe as mp

# # Initialize mediapipe
# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils
# hands = mp_hands.Hands()

# cap = cv2.VideoCapture(0)

# # Variables
# canvas = None
# mode = "Idle"
# tip_ids = [4, 8, 12, 16, 20]

# draw_enabled = False
# prev_fist = False

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     img = cv2.flip(img, 1)

#     if canvas is None:
#         canvas = img.copy() * 0

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     finger_count = 0

#     if results.multi_hand_landmarks:
#         for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

#             mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             landmarks = hand_landmarks.landmark
#             h, w, c = img.shape

#             lm_list = []
#             for lm in landmarks:
#                 lm_list.append((int(lm.x * w), int(lm.y * h)))

#             # 🔥 Detect hand type (Left/Right)
#             hand_label = results.multi_handedness[idx].classification[0].label

#             # 🔥 Thumb (fixed logic)
#             if hand_label == "Right":
#                 if lm_list[4][0] > lm_list[3][0]:
#                     finger_count += 1
#             else:  # Left hand
#                 if lm_list[4][0] < lm_list[3][0]:
#                     finger_count += 1

#             # 🔥 Other fingers
#             for i in range(1, 5):
#                 if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
#                     finger_count += 1

#             # 🔥 MODE SELECTION
#             if finger_count == 1:
#                 mode = "Drawing"
#             elif finger_count == 2:
#                 mode = "Counting"
#             elif finger_count == 0:
#                 mode = "Idle"

#             # 🔥 FIST TOGGLE (Drawing ON/OFF)
#             if finger_count == 0:
#                 if not prev_fist:
#                     draw_enabled = not draw_enabled
#                     prev_fist = True
#             else:
#                 prev_fist = False

#             # 🔥 DRAWING MODE
#             if mode == "Drawing" and draw_enabled:
#                 x = lm_list[8][0]
#                 y = lm_list[8][1]
#                 cv2.circle(canvas, (x, y), 8, (0, 0, 255), -1)

#             # 🔥 COUNTING MODE DISPLAY
#             if mode == "Counting":
#                 cv2.putText(img, f'Count: {finger_count}', (10, 100),
#                             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

#     # Merge drawing
#     img = cv2.add(img, canvas)

#     # Display mode
#     cv2.putText(img, f'Mode: {mode}', (10, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)

#     # Display drawing status
#     cv2.putText(img, f'Drawing: {draw_enabled}', (10, 150),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

#     cv2.imshow("Smart Hand System", img)

#     key = cv2.waitKey(1)
#     if key == ord('c'):
#         canvas = None
#     elif key & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()