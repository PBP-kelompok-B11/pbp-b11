from django.shortcuts import render, redirect, get_object_or_404
from nina_media_gallery.forms import MediaForm
from nina_media_gallery.models import Media
from django.http import HttpResponseRedirect

# Create your views here.

def gallery_list(request):
    media_list = Media.objects.all()
    
    context = {
        'media_list': media_list
    }

    return render(request, "list.html", context)

def gallery_upload(request):
    form = MediaForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('nina_media_gallery: show_all')
    
    context = {'form': form}
    return render(request, 'upload.html', context)

def gallery_details(request, id):
    media = get_object_or_404(Media, pk=id)
    media.increment_views()

    context = {
        'media': media
    }
    return render(request, 'media_detail.html', context)

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


def gallery_delete(request, id):
    media = get_object_or_404(Media, pk=id)
    media.delete()
    return HttpResponseRedirect()
