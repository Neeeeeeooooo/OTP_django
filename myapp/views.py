from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
import pyrebase
from django.contrib import messages
import logging
from django.http import JsonResponse
from django.contrib.auth import logout
# Firebase initialization
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
auth = firebase.auth()

# OTP generator function
def generate_otp():
    return str(random.randint(100000, 999999))

# Registration View
def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        try:
            # Attempt user creation in Firebase Authentication
            user = auth.create_user_with_email_and_password(email, password)
            otp = generate_otp()

            # Send OTP to email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            # Save OTP and email in session
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['role'] = role
            request.session['password'] = password

            # Save user info to Firebase Real-Time Database
            db = firebase.database()
            user_data = {
                'email': email,
                'role': role,
            }

            db.child("users").child(user['localId']).set(user_data)

            # Log the successful registration
            logging.info(f"User created with UID: {user['localId']}")
            return redirect('verify_otp')
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, 'register.html')


# OTP verification View
def verify_otp_view(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        
        # Check if OTP matches
        if otp == request.session.get('otp'):
            email = request.session.get('email')
            role = request.session.get('role')
            password = request.session.get('password')  # Retrieve password from session

            # User registration complete, log in and redirect to respective page
            try:
                # Sign in the user using Firebase Authentication
                user = auth.sign_in_with_email_and_password(email, password)
                if role == 'admin':
                     return redirect('admin')
                else:
                     return redirect('user')
            except Exception as e:
                logging.error(f"Error signing in user: {e}")
                return JsonResponse({"success": False, "message": "Login failed."})
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP"})

    return render(request, 'verify_otp.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            if role == 'admin':
                return redirect('admin')
            else:
                return redirect('user')
        except:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'login.html')

# User Interface View
def user_view(request):
    return render(request, 'user.html')

# Admin Interface View
def admin_view(request):
    return render(request, 'admin.html')

def logout_view(request):
    logout(request)  # This will log the user out
    return redirect('login')