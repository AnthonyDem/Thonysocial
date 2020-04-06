from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@login_required
def image_create(request):
    if request.method == 'POST':
        # form sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # data of form is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # Add user to created object
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # redirect user on saved image page
            return redirect(new_item.get_absolute_url())
        else:
            form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': 'form'})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image })

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id = image_id)
            if action == 'like':
                image.users_likes.add(request.user)
            else:
                image.users_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})