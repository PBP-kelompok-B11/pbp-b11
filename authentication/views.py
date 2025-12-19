from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt

# --- CUSTOM DECORATOR LOGIC ---

def check_is_admin(user):
    # Admin adalah superuser ATAU user yang memiliki UserProfile dengan role 'admin'
    if user.is_superuser:
        return True
    
    if hasattr(user, 'userprofile') and user.userprofile.role == 'admin':
        return True
    
    return False

def admin_only(view_func):
    """Decorator untuk membatasi view hanya bagi admin kustom kita."""
    decorated_view_funct = user_passes_test(
        check_is_admin, 
        login_url='authentication:login_view'
    )(view_func)
    return decorated_view_funct

# --- VIEWS ---
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        alamat = request.POST.get('alamat')
        umur = request.POST.get('umur')
        nomor_handphone = request.POST.get('nomor_handphone')
        role = request.POST.get('role')

        # Validasi
        if password != confirm_password:
            return JsonResponse({'success': False, 'message': "Password tidak cocok."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': "Username sudah digunakan."}, status=400)

        # Buat User
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        # Buat Profile
        UserProfile.objects.create(
            user=user,
            alamat=alamat,
            umur=umur,
            nomor_handphone=nomor_handphone,
            role=role,
        )

        # JANGAN REDIRECT! Kembalikan JSON Sukses
        return JsonResponse({
            'success': True,
            'message': "Akun berhasil dibuat! Silakan login.",
        }, status=201)

    # Hanya untuk GET request dari browser
    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    # 1. Cek apakah user sudah login
    if request.user.is_authenticated:
        # Jika request POST (dari Flutter/AJAX), langsung balas JSON, jangan REDIRECT
        if request.method == 'POST':
            return JsonResponse({
                'success': True,
                'message': f"Halo {request.user.username}, Anda sudah login!",
                'is_admin': check_is_admin(request.user),
                'username': request.user.username,
            })
        # Jika buka lewat browser biasa (GET), baru boleh redirect
        return redirect('authentication:home_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
<<<<<<< HEAD
            
            # SELALU balas JSON untuk POST request
            return JsonResponse({
                'success': True,
                'message': f"Halo {username}, selamat datang kembali!",
                'is_admin': check_is_admin(user),
                "username": user.username,
            })
=======

            # Kalau AJAX → balikin JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"Halo {username}, selamat datang kembali!",
                    'redirect_url': '',
                    "is_staff" : user.is_staff,
                    "username": user.username,
                    "user_id": user.id,
                })

            # Kalau normal → redirect biasa
            messages.success(request, f"Halo {username}, selamat datang kembali!")
            return redirect('authentication:home_view')

>>>>>>> 4a185a405e7ab7eedc5566a52cbab02ddcab34da
        else:
            # Balas JSON jika gagal
            return JsonResponse({
                'success': False,
                'message': "Username atau password salah."
            }, status=401)

    # Ini hanya untuk browser (GET request)
    return render(request, 'login.html')

@csrf_exempt
# JANGAN pakai @login_required agar tidak kena redirect otomatis ke /accounts/login/
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            "success": True,
            "message": "Kamu berhasil logout."
        }, status=200)
    
    # Jika user memang sudah tidak login, tetap kembalikan JSON sukses
    return JsonResponse({
        "success": True,
        "message": "Sudah tidak dalam sesi login."
    }, status=200)
def home_view(request):
    return render(request, 'home.html')

@login_required
def api_check_role(request):
    user = request.user
    role = "user" # Default
    
    if user.is_superuser:
        role = "admin"
    elif hasattr(user, 'userprofile'):
        role = user.userprofile.role

    return JsonResponse({"role": role})