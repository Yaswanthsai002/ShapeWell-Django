from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import AppUser


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
    # Check if the user has already entered their age, gender, height, and weight
    if not request.user.age or not request.user.gender or not request.user.height or not request.user.weight:
        # If the user has not entered their details yet, redirect to the collect page
        return redirect('collect')
    else:
        return redirect('levelselection')

    # If the user has already entered their details, render the profile template
    return render(request, 'profile.html', {'user': request.user})

@login_required
def t_knowledge(request):
    return render(request,'t-knowledge.html')

@login_required
def tree_knowledge(request):
    return render(request,'tree-knowledge.html')

@login_required
def warrior2_knowledge(request):
    return render(request,'warrior2-knowledge.html')

@login_required
def posedetection(request):
    return render(request,'posedetection.html')

@login_required
def plank_knowledge(request):
    return render(request,'plank-knowledge.html')

@login_required
def cobra_knowledge(request):
    return render(request,'cobra-knowledge.html')

@login_required
def triangle_knowledge(request):
    return render(request,'triangle-knowledge.html')

@login_required
def downdog_knowledge(request):
    return render(request,'downdog-knowledge.html')

@login_required
def warrior1_knowledge(request):
    return render(request,'warrior1-knowledge.html')

@login_required
def warrior3_knowledge(request):
    return render(request,'warrior3-knowledge.html')