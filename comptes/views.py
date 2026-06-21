from django.shortcuts import render, redirect
from .forms import InscriptionVendeurForm

def inscription_vendeur(request):
    if request.method == 'POST':
        form = InscriptionVendeurForm(request.POST)
        if form.is_valid():
            form.save()
            # Une fois inscrit, on le redirige vers une page de succès
            return render(request, 'comptes/succes.html')
    else:
        form = InscriptionVendeurForm()

    return render(request, 'comptes/inscription_vendeur.html', {'form': form})