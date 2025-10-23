from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def register_view(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': '/home/'})
        return redirect('authentication:home_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        alamat = request.POST.get('alamat')
        umur = request.POST.get('umur')
        nomor_handphone = request.POST.get('nomor_handphone')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if password != confirm_password:
                return JsonResponse({'success': False, 'message': "Password tidak cocok."})

            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': "Username sudah digunakan."})

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()

            # ✅ Simpan ke UserProfile
            UserProfile.objects.create(
                user=user,
                alamat=alamat,
                umur=umur,
                nomor_handphone=nomor_handphone
            )

            return JsonResponse({
                'success': True,
                'message': "Akun berhasil dibuat! Silakan login.",
                'redirect_url': '/login/'
            })

        # fallback non-AJAX
        if password != confirm_password:
            messages.error(request, "Password tidak cocok.")
            return redirect('authentication:register_view')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('authentication:register_view')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(
            user=user,
            alamat=alamat,
            umur=umur,
            nomor_handphone=nomor_handphone
        )

        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect('authentication:login_view')

    return render(request, 'register.html')

def login_view(request):
    # Kalau udah login, langsung ke home
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': '/home/'})
        return redirect('authentication:home_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Kalau AJAX → balikin JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"Halo {username}, selamat datang kembali!",
                    'redirect_url': '/home/'
                })

            # Kalau normal → redirect biasa
            messages.success(request, f"Halo {username}, selamat datang kembali!")
            return redirect('authentication:home_view')

        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': "Username atau password salah."
                }, status=400)

            messages.error(request, "Username atau password salah.")
            return redirect('authentication:login_view')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Kamu berhasil logout.")
    return redirect('authentication:login_view')

def home_view(request):
    return render(request, 'home.html')