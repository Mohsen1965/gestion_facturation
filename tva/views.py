from django.shortcuts import render, redirect, get_object_or_404
from .models import TVA
from .forms import TVAForm

# List all TVA entries
def list_tva(request):
    tva_list = TVA.objects.all()
    return render(request, 'tva/list_tva.html', {'tvas': tva_list})

# Create a new TVA entry
def create_tva(request):
    if request.method == 'POST':
        form = TVAForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_tva')  # Redirect to the list view
    else:
        form = TVAForm()
    
    return render(request, 'tva/create_tva.html', {'form': form})

def update_tva(request, tva_id):
    tva_instance = get_object_or_404(TVA, id=tva_id)
    if request.method == 'POST':
        form = TVAForm(request.POST, instance=tva_instance)
        if form.is_valid():
            form.save()
            return redirect('list_tva')  # Redirect to the list of TVA after saving the update
    else:
        form = TVAForm(instance=tva_instance)

    return render(request, 'tva/update_tva.html', {'form': form, 'tva': tva_instance})

# Delete an existing TVA entry
def delete_tva(request, tva_id):
    tva_instance = get_object_or_404(TVA, id=tva_id)
    if request.method == 'POST':
        tva_instance.delete()
        return redirect('list_tva')  # Redirect to the list view
    
    return render(request, 'tva/delete_tva.html', {'tva': tva_instance})
