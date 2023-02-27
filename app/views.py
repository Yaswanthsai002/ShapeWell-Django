from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import StreamingHttpResponse
from .models import AppUser
from app.pose_estimation import pose_estimation
import string
import mediapipe as mp
import pickle

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils

model, label_decoder = pickle.load(open('app/model.pkl', 'rb'))

def blog(request):
    return render(request, 'blog.html')


def type_of_user(request):
    return render(request, 'type_of_user.html')


def user_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        type_of_user = request.POST['user-type']

        # Check that the email is unique
        if AppUser.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.")

        # Check that the password and confirm password match
        elif password != confirm_password:
            messages.error(request, "The passwords do not match.")

        # Check that the password is at least 8 characters long
        elif len(password) < 8:
            messages.error(
                request, "The password must be at least 8 characters long.")

        # Check that the password is at most 16 characters long
        elif len(password) > 16:
            messages.error(
                request, "The password must be at most 16 characters long.")

        # Check that the password contains at least one lowercase letter
        elif not any(char.islower() for char in password):
            messages.error(
                request, "The password must contain at least one lowercase letter.")

        # Check that the password contains at least one uppercase letter
        elif not any(char.isupper() for char in password):
            messages.error(
                request, "The password must contain at least one uppercase letter.")

        # Check that the password contains at least one digit
        elif not any(char.isdigit() for char in password):
            messages.error(
                request, "The password must contain at least one digit.")

        # Check that the password contains at least one special character
        elif not any(char in string.punctuation for char in password):
            messages.error(
                request, "The password must contain at least one special character.")

        else:
            # If there are no errors, create the user and log them in
            user = AppUser.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=email, password=password, type_of_user=type_of_user)
            user.save()
            auth.login(request, user)
            messages.success(request, "Account created successfully!")
            messages.success(request, "Please signin to continue!")
            return redirect('user_signin')
        return redirect('user_signup')
    else:
        return render(request, 'user_signup.html')


def user_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.age != None:
                messages.success(request, "Successfully logged in!")
                return redirect('levelselection')
            else:
                messages.success(request, "Please enter your details.")
                return redirect('collect')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('user_signin')
    else:
        return render(request, 'user_signin.html')


def signout(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('user_signin')


def levelselection(request):
    return render(request, 'level_selection.html')


def beginner(request):
    return render(request, 'beginner.html')


def intermediate(request):
    return render(request, 'intermediate.html')


def advanced(request):
    return render(request, 'advanced.html')


def collect(request):
    if request.method == 'POST':
        # Get form data
        age = request.POST['age']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']

        # Validate form data
        if not age.isdigit():
            messages.error(request, "Age must be a number.")
            return redirect('collect')

        elif not height.isdigit():
            messages.error(request, "Height must be a number.")
            return redirect('collect')

        elif not weight.isdigit():
            messages.error(request, "Weight must be a number.")
            return redirect('collect')

        else:

            # If there are no errors, save the user's details
            user = request.user
            user.age = age
            user.gender = gender
            user.height = height
            user.weight = weight
            user.save()
            messages.success(request, "Details collected successfully!")
            return redirect('profile')

    # Check if the user has already entered their age, gender, height, and weight
    elif request.user.age and request.user.gender and request.user.height and request.user.weight:
        # If the user has already entered their details, redirect to the profile page
        return redirect('levelselection')
    else:
        return render(request, 'details_collection.html')


def profile(request):
    if not request.user.age or not request.user.gender or not request.user.height or not request.user.weight:
        return redirect('collect')
    else:
        return render(request, 'profile.html', {'user': request.user})


def warrior1_knowledge(request):
    return render(request, 'warrior1-knowledge.html')


def tree_knowledge(request):
    return render(request, 'tree-knowledge.html')


def warrior2_knowledge(request):
    return render(request, 'warrior2-knowledge.html')


def plank_knowledge(request):
    return render(request, 'plank-knowledge.html')


def cobra_knowledge(request):
    return render(request, 'cobra-knowledge.html')


def triangle_knowledge(request):
    return render(request, 'triangle-knowledge.html')


def downdog_knowledge(request):
    return render(request, 'downdog-knowledge.html')


def warrior1_knowledge(request):
    return render(request, 'warrior1-knowledge.html')


def warrior3_knowledge(request):
    return render(request, 'warrior3-knowledge.html')


def goddess_knowledge(request):
    return render(request, 'goddess-knowledge.html')


def posedetection(request):
    return StreamingHttpResponse(pose_estimation(model, label_decoder, mp_holistic, mp_drawing), content_type="multipart/x-mixed-replace;boundary=frame")


def result(request):
    return render(request, 'posedetection.html')
