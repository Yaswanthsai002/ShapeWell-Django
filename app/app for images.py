# Import required libraries.
import os
import pickle
import random
import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import pandas as pd

# Load the holistic model.
mp_holistic = mp.solutions.holistic

# Load the model and the label encoder from the pickle file
model, label_decoder = pickle.load(open('model.pkl', 'rb'))

# Create the holistic object for pose detection
holistic = mp_holistic.Holistic(static_image_mode=True, model_complexity=2)

# Set the path to the directory containing the asana folders
path = "app/DATASET/TEST"

# Initialize a resizable window.
# cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)

# Iterate through the asana folders
for asana in os.listdir(path):

    # Get the list of images in the asana folder
    images = os.listdir(os.path.join(path, asana))

    # Shuffle the list of images
    random.shuffle(images)

    # Take required images from the shuffled list
    images = images[:1]

    # Iterate through the images in the asana folder
    for image in images:

        # Set the path to the image
        image_path = os.path.join(path, asana, image)

        # Load the image
        img = cv2.imread(image_path)

        # Convert the image to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect the pose landmarks in the image
        results = holistic.process(imgRGB)

        # If pose landmarks were detected
        if results.pose_landmarks:

            # Create a data point from the pose landmarks
            row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility]
                       for landmark in results.pose_landmarks.landmark]).flatten())
            
            # Convert the list of landmarks in to a pandas dataframe.
            X = pd.DataFrame([row])

            # Predict the given landmarks.
            asana_class = label_decoder.inverse_transform(model.predict(X))[0]

            # To know the prediction probability of all classes.
            asana_prob = model.predict_proba(X)[0]

            # Get the score of the asana whic has highest probability.
            asana_score = int(round(asana_prob[np.argmax(asana_prob)], 2)*100)

            # Resize the frame in required height and width.
            img = cv2.resize(img, (500, 500))

            # Check if the predicted class has a probability or a score greater than 80 out of 100.
            if asana_score >= 90:
                
                # Draw a green color filled rectangle to put the asana class and asana score
                cv2.rectangle(img, (0, 0), (400, 80), (0, 255, 0), -1)
                
                cv2.putText(img, 'Asana',
                            (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)  
                
                # Put the asana class and asana score in the rectangle.
                cv2.putText(img, f'{asana_class}',
                            (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)               
                
                cv2.putText(img, 'Score',
                            (300, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                
                cv2.putText(img, f'{asana_score}',
                            (300, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            
            # If the predicted class doesn't have a required threshold.
            else:
                
                # Draw a red color filled rectangle to put the asana class and asana score
                cv2.rectangle(img, (0, 0), (400, 80), (255, 0, 0), -1)
                
                cv2.putText(img, 'Asana',
                            (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)  
                
                # Put the asana class and asana score in the rectangle.
                cv2.putText(img, f'{asana_class}',
                            (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)               
                
                cv2.putText(img, 'Score',
                            (300, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                
                cv2.putText(img, f'{asana_score}',
                            (300, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            
            # Display the image.
            # cv2.imshow('Pose Classification',img)

            # Wait until a key is pressed.
            # Retreive the ASCII code of the key pressed
            # k = cv2.waitKey(10000) & 0xFF

            # Check if key is pressed.
            # if (k == 27):
                # break

            # Destroy all the windows opened by opencv.
            # cv2.destroyAllWindows()

            # Turn of the axis. 
            plt.axis('off')
            
            # Plot the image.
            plt.imshow(img)

            # Show thw image.
            plt.show()

            # Check if the folder exist, if not create a folder. 
#             if not os.path.exists("output_folder"):
            
            # Create a folder.
#                 os.makedirs("output_folder")
            
            # Save the image in the folder.
#             cv2.imwrite(os.path.join("output_folder", image), img)