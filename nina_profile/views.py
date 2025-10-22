import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import ProfileWidget
from .forms import ProfileWidgetForm

def is_admin(user):
    return user.is_active and user.is_staff

# Halaman overview untuk setiap profil (Player / Club)
def profile_overview(request, target_model, pk):
    content_type = get_object_or_404(ContentType, model=target_model)
    profile = get_object_or_404(content_type.model_class(), pk=pk)
    widgets = ProfileWidget.objects.filter(content_type=content_type, object_id=pk)

    return render(request, 'overview.html', {
        'profil': profile,
        'widgets': widgets,
        'content_type': content_type.id,
        'object_id': pk,
    })

# Daftar semua widget (hanya admin)
@login_required
@user_passes_test(is_admin)
def widget_list(request):
    widgets = ProfileWidget.objects.all()
    return render(request, 'list.html', {'widgets': widgets})

# Create Widget
@login_required
@user_passes_test(is_admin)
def widget_create(request, content_type_id=None, object_id=None):
    if request.method == 'POST':
        form = ProfileWidgetForm(request.POST)
        if form.is_valid():
            widget = form.save(commit=False)
            
            # Set relasi ke profil target (Player atau Club)
            if content_type_id and object_id:
                widget.content_type = ContentType.objects.get(id=content_type_id)
                widget.object_id = object_id

            widget.created_by = request.user
            widget.save()
            return JsonResponse({
                'status': 'success',
                'id': widget.id,
                'title': widget.title,
                'content': widget.content or '',
                'widget_type': widget.widget_type
            })

        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    form = ProfileWidgetForm()
    return render(request, 'form.html', {'form': form})

# Update Widget
@login_required
@user_passes_test(is_admin)
def widget_update(request, pk):
    widget = get_object_or_404(ProfileWidget, pk=pk)
    if request.method == 'POST':
        form = ProfileWidgetForm(request.POST, instance=widget)
        if form.is_valid():
            widget = form.save()
            return JsonResponse({
                'status': 'success',
                'id': widget.id,
                'title': widget.title,
                'content': widget.content or '',
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    form = ProfileWidgetForm(instance=widget)
    return render(request, 'form.html', {'form': form, 'widget': widget})

# Delete Widget
@login_required
@user_passes_test(is_admin)
def widget_delete(request, pk):
    widget = get_object_or_404(ProfileWidget, pk=pk)
    if request.method == 'POST':
        widget.delete()
        return JsonResponse({'status': 'success', 'id': pk})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def get_chart_data(request, widget_id):
    widget = get_object_or_404(ProfileWidget, id=widget_id)
    config = widget.konfigurasi

    model_name = widget.content_type.model

    if model_name == "player":
        file_path = os.path.join(settings.BASE_DIR, 'data', 'players_stats.csv')
        