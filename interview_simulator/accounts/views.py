from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_or_signup_view(request):
    if request.method == 'POST':
        # Login Logic
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.error(request, 'Please fill in all fields.')
            else:
                # Authenticate user
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/chat/')  # Redirect to the chat app
                else:
                    messages.error(request, 'Invalid username or password.')

        # Signup Logic
        elif 'signup' in request.POST:
            username = request.POST.get('signup-username')
            password = request.POST.get('signup-password')
            confirm_password = request.POST.get('signup-confirm-password')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif password != confirm_password:
                messages.error(request, 'Passwords do not match.')
            else:
                # Create user and save
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Signup successful! You can now log in.')
                return redirect('login')  # Redirect to login page after signup

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out. Please log in first.")
    return redirect('login')
