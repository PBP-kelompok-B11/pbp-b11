from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register_view(request):
    # Kalau user udah login, langsung lempar ke home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

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
        return redirect('login')  # ✅ redirect ke halaman login

    return render(request, 'authentication/register.html')


def login_view(request):
    # Kalau user udah login, langsung ke home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Halo {username}, selamat datang kembali!")
            return redirect('home')  # ✅ redirect ke home setelah login
        else:
            messages.error(request, "Username atau password salah.")
            return redirect('login')

    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Kamu berhasil logout.")
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')
