from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from nina_media_gallery.forms import MediaForm
from nina_media_gallery.models import Media
from django.http import HttpResponseRedirect, JsonResponse

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

    context = {
        'media': media
    }
    return render(request, 'media_detail.html', context)

def get_gallery_items(request):
    """API endpoint untuk mengambil semua media items"""
    try:
        media_items = Media.objects.all()
        data = []
        
        for item in media_items:
            data.append({
                'id': item.id,
                'deskripsi': item.deskripsi,
                'category': item.category,
                'thumbnail': item.thumbnail if item.thumbnail else '',
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(item, 'created_at') else ''
            })
        
        return JsonResponse({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# @user_passes_test(is_admin)
def gallery_upload(request):
    try:
        deskripsi = request.POST.get('deskripsi')
        category = request.POST.get('category')
        thumbnail = request.POST.get('thumbnail')

        new_media = Media(
            deskripsi=deskripsi,
            category=category,
            thumbnail=thumbnail
        )
        new_media.save()
        return JsonResponse({
                'status': 'success',
                'message': 'Media uploaded successfully!',
                'data': {
                    'id': new_media.id,
                    'description': new_media.deskripsi,
                    'category': new_media.category,
                    'thumbnail': str(new_media.thumbnail)
                }
            }, status=201)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
@user_passes_test(is_admin)
def gallery_update(request, id):
    media = get_object_or_404(Media, pk=id)
    form = MediaForm(request.POST or None, instance=media)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('nina_media_gallery:gallery_list')
    
    context = {
        'form': form
    }

    return render(request, 'form.html', context)

@user_passes_test(is_admin)
def gallery_delete(request, id):
    media = get_object_or_404(Media, pk=id)
    media.delete()
    return redirect('nina_media_gallery:gallery_list')

