from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
#tes commit
        if password != confirm_password:
            messages.error(request, "Password tidak cocok.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect('login')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('search_form')  
        else:
            messages.error(request, "Username atau password salah.")
            return redirect('login')

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Kamu berhasil logout.")
    return redirect('login')
