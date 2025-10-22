from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import ProfileWidget
from .forms import ProfileWidgetForm

# Create your views here.

def is_admin(user):
    return user.is_active and user.is_staff

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

@login_required
@user_passes_test(is_admin)
def widget_list(request):
    widgets = ProfileWidget.objects.all()
    return render(request, 'list.html', {'widgets': widgets})

# method khusus admin yaitu menambahkan widget
@login_required
@user_passes_test(is_admin)
def widget_create(request):
    if request.method == 'POST':
        form = ProfileWidgetForm(request.POST)
        if form.is_valid():
            widget = form.save(commit=False)
            widget.created_by = request.user
            widget.save()
            return JsonResponse({
                'status': 'success',
                'id': widget.id, 
                'title': widget.title,
                'content': widget.content,
            })
        else:
            return JsonResponse({'status': 'error'}, status=400)
    
    form = ProfileWidgetForm()
    return render(request, 'form.html', {'form': form})

# method khusus untuk admin yaitu memperbarui widget
@login_required
@user_passes_test(is_admin)
def widget_update(request, pk):
    widget = get_object_or_404(ProfileWidget, pk=pk)
    if request.method == 'POST':
        form = ProfileWidgetForm(request.POST, instance=widget)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'id': widget.id,
                'title': widget.title,
                'content': widget.content,
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.error}, status=400)

    form = ProfileWidgetForm(instance=widget)
    return render(request, 'form.html', {'form': form, 'widget': widget})

@login_required
@user_passes_test(is_admin)
def widget_delete(request, pk):
    widget = get_object_or_404(ProfileWidget, pk=pk)
    if request.method == 'POST':
        widget.delete()
        return JsonResponse({'status': 'success', 'message': 'Succesfully deleted the widget', 'id': pk})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
