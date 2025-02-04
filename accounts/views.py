from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        return redirect('profile')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'user_profile': user_profile})


#edit profile
@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save(user=user)
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = UserProfileForm(instance=profile, user=user)

    return render(request, 'accounts/edit_profile.html', {'form': form})
