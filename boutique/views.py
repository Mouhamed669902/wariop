from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produit, Commande, ProfilVendeur
from .forms import AjouterProduitForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.dateparse import parse_date
from django.db.models import Q # <--- Importe Q en haut du fichier


# 1. Accueil avec recherche
def liste_produits(request):
    # On commence avec les produits disponibles
    produits = Produit.objects.filter(disponible=True)

    # On récupère la recherche depuis l'URL (ex: ?q=iphone)
    query = request.GET.get('q')

    if query:
        # On ajoute le filtre de recherche au filtre de disponibilité
        produits = produits.filter(
            Q(nom__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'boutique/index.html', {'produits': produits, 'query': query})

# 2. Ajout de produit (Vendeur)
@login_required(login_url='/comptes/login/')
def ajouter_produit(request):
    try:
        profil_vendeur = ProfilVendeur.objects.get(user=request.user)
    except ProfilVendeur.DoesNotExist:
        return render(request, 'boutique/erreur_vendeur.html', {
            'message': "Vous n'avez pas de profil vendeur. Contactez l'administrateur."
        })
    if not profil_vendeur.est_approuve:
        return render(request, 'boutique/erreur_vendeur.html', {
            'message': "Votre boutique est en attente de validation."
        })
    if request.method == 'POST':
        form = AjouterProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.vendeur = profil_vendeur
            produit.save()
            return redirect('liste_produits')
    else:
        form = AjouterProduitForm()
    return render(request, 'boutique/ajouter_produit.html', {'form': form})

# 3. Panier : Ajout
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier = request.session.get('panier', {})
    id_str = str(produit_id)
    if id_str in panier:
        panier[id_str]['quantite'] += 1
    else:
        panier[id_str] = {
            'nom': produit.nom,
            'prix': float(produit.prix),
            'quantite': 1
        }
    request.session['panier'] = panier
    request.session.modified = True
    return redirect('voir_panier')

# 4. Panier : Affichage
def voir_panier(request):
    panier = request.session.get('panier', {})
    articles_panier = []
    total_panier = 0
    for id_str, infos in panier.items():
        sous_total = float(infos['prix']) * infos['quantite']
        total_panier += sous_total
        articles_panier.append({
            'id': id_str,
            'nom': infos['nom'],
            'prix': infos['prix'],
            'quantite': infos['quantite'],
            'total_produit': sous_total,
        })
    return render(request, 'boutique/panier.html', {
        'articles_panier': articles_panier,
        'total_panier': total_panier
    })

# 5. Panier : Modification quantité
def modifier_quantite(request, produit_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        id_str = str(produit_id)
        if id_str in panier:
            nouvelle_qte = int(request.POST.get('quantite', 1))
            if nouvelle_qte > 0:
                panier[id_str]['quantite'] = nouvelle_qte
            else:
                del panier[id_str]
            request.session['panier'] = panier
            request.session.modified = True
    return redirect('voir_panier')

# 6. Panier : Suppression
def supprimer_du_panier(request, produit_id):
    panier = request.session.get('panier', {})
    id_str = str(produit_id)
    if id_str in panier:
        del panier[id_str]
        request.session['panier'] = panier
        request.session.modified = True
    return redirect('voir_panier')

# 7. Panier : Vider tout
def vider_panier(request):
    if 'panier' in request.session:
        del request.session['panier']
        request.session.modified = True
    return redirect('voir_panier')

# 8. Commande
def valider_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('liste_produits')

    total = sum(float(item['prix']) * item['quantite'] for item in panier.values())

    if request.method == 'POST':
        # On récupère les données du formulaire HTML
        nom_complet = request.POST.get('nom_complet')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        # Création de l'objet Commande dans la base de données
        commande = Commande.objects.create(
            nom_complet=nom_complet,
            telephone=telephone,
            adresse_livraison=adresse,
            total=total,
            resume_produits="\n".join([f"- {item['nom']} (x{item['quantite']})" for item in panier.values()])
        )

        # Une fois la commande enregistrée, on vide le panier
        del request.session['panier']
        request.session.modified = True

        # Redirection vers une page de confirmation
        return render(request, 'boutique/confirmation.html', {'commande': commande})

    # Si c'est une requête GET, on affiche simplement le formulaire
    return render(request, 'boutique/valider_commande.html', {'total': total})


# Fonction qui vérifie si l'utilisateur est admin
def est_admin(user):
    return user.is_staff


@user_passes_test(est_admin, login_url='/comptes/login/')
def dashboard_admin(request):
    # 1. Compter le nombre total de commandes
    total_commandes = Commande.objects.count()

    # 2. Calculer le revenu total (somme du champ 'total' de chaque commande)
    revenus_totaux = sum(c.total for c in Commande.objects.all())

    # 3. Récupérer les 5 dernières commandes, de la plus récente à la plus ancienne
    dernieres_commandes = Commande.objects.all().order_by('-date_creation')[:5]

    # 4. Envoyer tout cela au template
    return render(request, 'boutique/dashboard.html', {
        'total_commandes': total_commandes,
        'revenus_totaux': revenus_totaux,
        'dernieres_commandes': dernieres_commandes
    })


@user_passes_test(est_admin, login_url='/comptes/login/')
def dashboard_admin(request):
    # Récupérer les dates depuis les paramètres GET (URL)
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    commandes = Commande.objects.all()

    # Filtrer si les dates sont fournies
    if date_debut:
        commandes = commandes.filter(date_creation__gte=date_debut)
    if date_fin:
        commandes = commandes.filter(date_creation__lte=date_fin)

    total_commandes = commandes.count()
    revenus_totaux = sum(c.total for c in commandes)

    return render(request, 'boutique/dashboard.html', {
        'total_commandes': total_commandes,
        'revenus_totaux': revenus_totaux,
        'dernieres_commandes': commandes.order_by('-date_creation')[:10],
        'date_debut': date_debut,
        'date_fin': date_fin
    })


@user_passes_test(est_admin)
def changer_statut_commande(request, commande_id, nouveau_statut):
    # On cherche la commande ou on renvoie une erreur 404 si elle n'existe pas
    commande = get_object_or_404(Commande, id=commande_id)

    # On met à jour le statut
    commande.statut = nouveau_statut
    commande.save()

    # On redirige vers le dashboard pour voir la mise à jour
    return redirect('dashboard_admin')