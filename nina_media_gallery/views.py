from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
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

# @user_passes_test(is_admin)
def gallery_upload(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Media berhasil diupload!"})
        else:
            return JsonResponse({"status": "error", "message": "Form tidak valid!"})
        
    form = MediaForm()
    return render(request, 'upload.html', {'form': form})

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
