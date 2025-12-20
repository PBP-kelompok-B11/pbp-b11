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
            
            # 1. CEK APAKAH INI DARI FLUTTER?
            # Flutter biasanya mengirim 'is_flutter' atau header khusus
            if request.POST.get('is_flutter') == 'true' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"Halo {username}, selamat datang kembali!",
                    'is_admin': check_is_admin(user),
                    'username': user.username,
                    'user_id': user.id,
                })
            
            # 2. JIKA DARI WEB BIASA, REDIRECT KE HOME
            messages.success(request, f"Halo {username}, selamat datang kembali!")
            return redirect('authentication:home_view') # Ini akan membuka home.html, bukan JSON
        else:
            # Balas JSON jika gagal
            return JsonResponse({
                'success': False,
                'message': "Username atau password salah."
            }, status=401)
    # Ini hanya untuk browser (GET request)
    return render(request, 'login.html')

@csrf_exempt
def logout_view(request):
    username = request.user.username # Simpan nama user sebelum logout untuk pesan
    logout(request) 
    
    # 1. Cek apakah request berasal dari Flutter atau AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('is_flutter') == 'true':
        return JsonResponse({
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)

    # 2. Jika diakses via Browser biasa, arahkan ke halaman login atau home
    messages.success(request, "Kamu berhasil logout.")
    return redirect('authentication:login_view') # Arahkan kembali ke halaman login web0)
    

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


@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    user = authenticate(
        request,
        username=request.POST.get('username'),
        password=request.POST.get('password'),
    )

    if user is None:
        return JsonResponse({'success': False}, status=401)

    login(request, user)

    return JsonResponse({
        'success': True,
        'username': user.username,
        'is_admin': check_is_admin(user),
    })

@csrf_exempt
def api_logout(request):
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Logout berhasil'
    })

