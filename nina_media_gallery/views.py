from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from nina_media_gallery.forms import MediaForm
from nina_media_gallery.models import Media
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.
def is_admin(user):
    return user.is_authenticated and user.is_staff

def gallery_list(request):
    media_list = Media.objects.all()
    
    context = {
        'media_list': media_list
    }

    return render(request, "gallery_list.html", context)

def gallery_details(request, id):
    media = get_object_or_404(Media, pk=id)
    media.increment_views()
    
    # Get all media ordered by created_at
    all_media = Media.objects.all().order_by('created_at')
    media_list = list(all_media)
    
    # Find current index
    try:
        current_index = media_list.index(media)
        
        # Get previous and next
        previous_media = media_list[current_index - 1] if current_index > 0 else None
        next_media = media_list[current_index + 1] if current_index < len(media_list) - 1 else None
    except ValueError:
        previous_media = None
        next_media = None

    context = {
        'media': media,
        'previous_media': previous_media,
        'next_media': next_media,
    }
    return render(request, 'media_detail.html', context)
def get_gallery_items(request):
   def get_gallery_items(request):
    media = Media.objects.all().values('deskripsi', 'media_file')
    data = [
        {
            "deskripsi": item['deskripsi'],
            "image_url": "/media/" + item['media_file']  # Sesuaikan MEDIA_URL
        }
        for item in media
    ]
    return JsonResponse(data, safe=False)

# @user_passes_test(is_admin)
def gallery_upload(request):
    if request.method == "POST":
        # Handle AJAX upload
        form = MediaForm(request.POST)
        
        # Debug: Print POST data
        print("POST data:", request.POST)
        
        if form.is_valid():
            try:
                new_media = form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Media uploaded successfully!',
                    'data': {
                        'id': str(new_media.id),
                        'description': new_media.deskripsi,
                        'category': new_media.category,
                        'thumbnail': str(new_media.thumbnail) if new_media.thumbnail else None
                    }
                }, status=201)
            except Exception as e:
                import traceback
                print(f"Save Error: {str(e)}")
                print(traceback.format_exc())
                return JsonResponse({
                    'status': 'error',
                    'message': f'An error occurred: {str(e)}'
                }, status=500)
        else:
            # Form tidak valid, kembalikan error
            print("Form errors:", form.errors)
            return JsonResponse({
                'status': 'error',
                'message': 'Form validation failed',
                'errors': form.errors
            }, status=400)
    
    # Handle GET request - render form page
    else:
        form = MediaForm()
        context = {
            'form': form
        }
        return render(request, 'upload.html', context)
    
def gallery_update(request, id):
    if request.method == 'POST':
        media = Media.objects.get(pk=id)
        media.deskripsi = request.POST.get('deskripsi')
        media.category = request.POST.get('category')
        media.thumbnail = request.POST.get('thumbnail')
        media.save()

        return JsonResponse({
            "status": "success",
            "media": {
                "deskripsi": media.deskripsi,
                "category_display": media.get_category_display(),
                "thumbnail": media.thumbnail,
            }
        })
    return JsonResponse({"status": "error", "message": "Invalid request"})

def gallery_delete(request, id):
    media = get_object_or_404(Media, pk=id)
    media.delete()
    return HttpResponseRedirect(reverse('nina_media_gallery:gallery_list'))

