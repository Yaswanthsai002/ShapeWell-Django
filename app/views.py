from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import StreamingHttpResponse
from .models import AppUser

import math
import cv2
import mediapipe as mp
import pyautogui
from time import time

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check that the username is unique
        if AppUser.objects.filter(username=user_name).exists():
            messages.error(
                request, "A user with that username already exists.")

        # Check that the email is unique
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.")

        # Check that the password and confirm password match
        if password != confirm_password:
            messages.error(request, "The passwords do not match.")

        # Check that the password is at least 8 characters long
        if len(password) < 8:
            messages.error(
                request, "The password must be at least 8 characters long.")

        # Check that the username and password are alphanumeric
        if not user_name.isalnum():
            messages.error(request, "The username must be alphanumeric.")
        if not password.isalnum():
            messages.error(request, "The password must be alphanumeric.")

        # If there are no errors, create the user and log them in
        user = AppUser.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=user_name, password=password)
        user.save()
        auth.login(request, user)
        messages.success(request, "Account created successfully!")
        messages.success(request, "Please signin to continue.")
        return redirect('signin')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('collect')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required
def signout(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('signin')

@login_required
def levelselection(request):
    return render(request, 'levelselection.html')

@login_required
def beginner(request):
    return render(request, 'beginner.html')

@login_required
def intermediate(request):
    return render(request, 'intermediate.html')

@login_required
def expert(request):
    return render(request, 'expert.html')

@login_required
def collect(request):

    # Check if the user has already entered their age, gender, height, and weight
    if request.user.age and request.user.gender and request.user.height and request.user.weight:
        # If the user has already entered their details, redirect to the profile page
        return redirect('levelselection')

    if request.method == 'POST':
        # Get form data
        messages.success(request, "Please enter your details!")
        age = request.POST['age']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']

        # Validate form data
        if not age.isdigit():
            messages.error(request, "Age must be a number.")
            return redirect('collect')

        if not height.isdigit():
            messages.error(request, "Height must be a number.")
            return redirect('collect')

        if not weight.isdigit():
            messages.error(request, "Weight must be a number.")
            return redirect('collect')

        # If there are no errors, save the user's details
        user = request.user
        user.age = age
        user.gender = gender
        user.height = height
        user.weight = weight
        user.save()
        messages.success(request, "Details collected successfully!")
        return redirect('profile')
    else:
        return render(request, 'collectdetails.html')

@login_required
def profile(request):
    if not request.user.age or not request.user.gender or not request.user.height or not request.user.weight:
        return redirect('collect')
    else:
        return redirect('levelselection')
    return render(request, 'profile.html', {'user': request.user})

@login_required
def t_knowledge(request):
    return render(request, 't-knowledge.html')

@login_required
def tree_knowledge(request):
    return render(request, 'tree-knowledge.html')

@login_required
def warrior2_knowledge(request):
    return render(request, 'warrior2-knowledge.html')

@login_required
def plank_knowledge(request):
    return render(request, 'plank-knowledge.html')

@login_required
def cobra_knowledge(request):
    return render(request, 'cobra-knowledge.html')

@login_required
def triangle_knowledge(request):
    return render(request, 'triangle-knowledge.html')

@login_required
def downdog_knowledge(request):
    return render(request, 'downdog-knowledge.html')

@login_required
def warrior1_knowledge(request):
    return render(request, 'warrior1-knowledge.html')

@login_required
def warrior3_knowledge(request):
    return render(request, 'warrior3-knowledge.html')

@login_required
# Pose Estimation
def gen_frames(request):

    # Setup Holistic Pose function for video.
    pose_video = mp_holistic.Holistic(
        static_image_mode=False, min_detection_confidence=0.5, model_complexity=2)

    screen_width, screen_height = pyautogui.size()

    # Initialize the VideoCapture object to read from the webcam.
    camera_video = cv2.VideoCapture(0)

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

        # Resize the frame.
        # frame = cv2.resize(frame, (screen_width, screen_height))

        # # Perform Pose landmark detection.
        # frame, landmarks = detectPose(frame, pose_video)

        # # Check if the landmarks are detected.
        # if landmarks:

        #     # Perform the Pose Classification.
        #     frame, _ = classifyPose(landmarks, frame)

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

@login_required
def posedetection(request):
    return StreamingHttpResponse(gen_frames(request), content_type="multipart/x-mixed-replace;boundary=frame")

@login_required
def result(request):
    return render(request, 'posedetection.html')