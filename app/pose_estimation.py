import cv2
from time import time
import mediapipe as mp
import pyautogui
import numpy as np
import pickle
import pandas as pd

model, label_decoder = pickle.load(open('app/model.pkl', 'rb'))

# Initializing mediapipe pose class.
mp_holistic = mp.solutions.holistic

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils


# Pose Estimation
def pose_estimation(model, label_decoder, mp_holistic, mp_drawing):

    # Setup Holistic Pose function for video.
    holistic = mp_holistic.Holistic(
        static_image_mode=False, model_complexity=2)

    screen_width, screen_height = pyautogui.size()

    # Initialize the VideoCapture object to read from the webcam.
    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, screen_width)
    camera_video.set(4, screen_height)

    # Initialize a resizable window.
    cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)

    start_time = time()

    # Initialize a variable to store the number of frames processed.
    num_frames = 0

    # Iterate until the webcam is accessed successfully.
    while camera_video.isOpened():

        # Read a frame.
        ok, frame = camera_video.read()

        # Check if frame is not read properly.
        if not ok:

            # Continue to the next iteration to read the next frame and ignore the empty camera frame.
            continue

        # Flip the frame horizontally for natural (selfie-view) visualization.
        frame = cv2.flip(frame, 1)

        # Resize the frame while keeping the aspect ratio.
        frame = cv2.resize(frame, (screen_width, screen_height))

        results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Check if the landmarks are detected.
        if results.pose_landmarks:

            # Add all the landmarks of keypoints to a list for prediction.
            row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility]
                       for landmark in results.pose_landmarks.landmark]).flatten())

            # Convert the list into a pandas dataframe.
            X = pd.DataFrame([row])

            # Predict the given landmarks.
            asana_class = label_decoder.inverse_transform(model.predict(X))[0]

            # To know the prediction probability of all classes.
            asana_prob = model.predict_proba(X)[0]

            # Get the score of the asana whic has highest probability.
            asana_score = int(round(asana_prob[np.argmax(asana_prob)], 2)*100)

            # Check if the predicted class has a probability or a score greater than 80 out of 100.
            # If the predicted class has a probablity greater than then 80 the Asana done is correct and the body landmarks will turn into green in colour.
            if asana_score >= 80:

                # Draw a green colour filled rectangle to put the asana name and score in it.
                cv2.rectangle(frame, (0, 0), (400, 75), (0, 255, 0), -1)

                # Put the asana label and the asana score in the rectangle.
                cv2.putText(frame, f'{asana_class} {asana_score}',
                            (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

                # Draw the landmarks
                # 2. Right hand
                mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
                                            )

                # 3. Left Hand
                mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
                                            )

                # 4. Pose Detections
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(255, 255, 255), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(
                                              color=(0, 255, 0), thickness=2, circle_radius=2)
                                          )

            # if the predicted class has a probability or a score lesser than 80 out of 100.
            # If the predicted class has a probablity lesser than then 80 the Asana done is wrong and the body landmarks will turn into red in colour.
            else:
                
                # Draw a red colour filled rectangle to put the asana name and score in it.
                cv2.rectangle(frame, (0, 0), (400, 75), (0, 0, 255), -1)

                # Put the asana label and the asana score in the rectangle.
                cv2.putText(frame, f'{asana_class} {asana_score}',
                            (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

                # Draw the landmarks
                # 2. Right hand
                mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                                        )

                # 3. Left Hand
                mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                                        )

                # 4. Pose Detections
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(255, 255, 255), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(
                                              color=(0, 0, 255), thickness=2, circle_radius=2)
                                          )
        # If no landmarks are detected then pass.
        else:
            pass

        # Increment the number of frames processed.
        num_frames += 1

        # Get the elapsed time.
        elapsed_time = time() - start_time

        # Calculate the frames per second.
        fps = num_frames / elapsed_time

        # Write the calculated number of frames per second on the frame.
        cv2.putText(frame, 'FPS: {}'.format(int(fps)), (0, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # concat frame one by one and show result
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Display the frame.
        # cv2.imshow('Pose Classification', frame)

        # Wait until a key is pressed.
        # Retreive the ASCII code of the key pressed
        # k = cv2.waitKey(1) & 0xFF

        # if (k == 27):
            # break

    # Release the video object.
    # camera_video.release()

    # Destroy all the windows.
    # cv2.destroyAllWindows()

# pose_estimation(model, label_decoder, mp_holistic, mp_drawing)