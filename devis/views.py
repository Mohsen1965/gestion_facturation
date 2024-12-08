from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, TVA, Devis, LigneDevis
from .forms import DevisForm, LigneDevisFormSet  # Ensure you have this import
from client.models import Client
from article.models import Article
from django.http import JsonResponse
from django.utils import timezone
import logging
from django.contrib import messages
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from decimal import Decimal, InvalidOperation
from django.template.loader import render_to_string
from django.db.models import Max


def generate_devis_pdf(request, devis_id):
    # Créez l'objet HttpResponse avec l'en-tête PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="devis_{devis_id}.pdf"'
    
    # Créez le PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Obtenez la largeur et la hauteur de la page

    # Récupérez la devis et les lignes associées
    devis = get_object_or_404(Devis, id=devis_id)
    ligne_devis = LigneDevis.objects.filter(devis=devis)

    # Initialisez la position de départ et le numéro de page
    x = 50
    y = height - 50
    page_number = 1

    # Fonction pour dessiner l'en-tête
    def draw_header():
        nonlocal y
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(x, y, "Mohsen GHARBI GAMMOUDA Services")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y - 20, "20 Av. Habib Bourguiba, Sidi Bouzid")
        pdf.drawString(x, y - 40, "Tel: 76 625 788 - 98 417 237")
        pdf.drawString(x, y - 60, "Email: gmohsen6@gmail.com")
        pdf.drawString(x, y - 80, "MF: 0421452S")
        pdf.drawString(x, y - 100, "RIB: 4663")
        y -= 160

    # Fonction pour dessiner le pied de page avec le numéro de page
    def draw_footer():
        pdf.setFont("Helvetica", 10)
        pdf.drawString(width - 100, 30, f"Page {page_number}")

    # Fonction pour dessiner les totaux
    def draw_totals():
        nonlocal y
        pdf.setFont("Helvetica-Bold", 12)
        y -= 10
        pdf.drawString(x + 300, y, "Total HT:")
        pdf.drawString(x + 370, y, f"{total_general_ht:.3f}")
        y -= 20
        pdf.drawString(x + 300, y, "Total TVA:")
        pdf.drawString(x + 370, y, f"{total_general_tva:.3f}")
        y -= 20
        pdf.drawString(x + 300, y, "Total TTC:")
        pdf.drawString(x + 370, y, f"{total_general_ttc:.3f}")

    # Commencez la première page
    draw_header()

    # Détails de la devis
    pdf.drawString(x, y, f"Devis No: {devis.numero_devis}")
    pdf.drawString(x, y - 20, f"Date: {devis.date_devis.strftime('%d/%m/%Y')}")
    pdf.drawString(x, y - 40, f"Client: {devis.client}")
    y -= 80

    # En-tête du tableau des articles
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Article")
    pdf.drawString(x + 150, y, "Qté")
    pdf.drawString(x + 220, y, "P.U")
    pdf.drawString(x + 300, y, "Rem %")
    pdf.drawString(x + 350, y, "Net. HT")
    pdf.drawString(x + 450, y, "TVA %")
    pdf.line(x, y - 5, width - 50, y - 5)
    y -= 25

    # Réinitialisez la police pour les lignes d'articles
    pdf.setFont("Helvetica", 8)

    # Initialisez les totaux
    total_general_ht = Decimal('0')
    total_general_tva = Decimal('0')
    total_general_ttc = Decimal('0')
    tva_totals = {}

    # Ajoutez les lignes d'articles
    for ligne in ligne_devis:
        if y < 50:  # Si on atteint le bas de la page, ajoutez une nouvelle page
            draw_footer()
            pdf.showPage()
            y = height - 50
            page_number += 1
            draw_header()
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(x, y, "Article")
            pdf.drawString(x + 150, y, "Qté")
            pdf.drawString(x + 220, y, "P.U")
            pdf.drawString(x + 300, y, "Rem %")
            pdf.drawString(x + 350, y, "Net. HT")
            pdf.drawString(x + 450, y, "TVA %")
            pdf.line(x, y - 5, width - 50, y - 5)
            y -= 25
            pdf.setFont("Helvetica", 8)

        pdf.drawString(x, y, str(ligne.article))
        pdf.drawString(x + 150, y, str(ligne.quantite))
        pdf.drawString(x + 220, y, f"{ligne.prix_unitaire:.3f}")
        pdf.drawString(x + 300, y, f"{ligne.taux_remise:.3f} %")

        # Calculs des montants
        total_ht = ligne.quantite * ligne.prix_unitaire * (1 - ligne.taux_remise / 100)
        total_general_ht += total_ht
        tva_obj = get_object_or_404(TVA, id=ligne.article.tva_id)
        total_tva = total_ht * (tva_obj.taux_tva / 100)
        total_general_tva += total_tva
        total_ttc = total_ht + total_tva
        total_general_ttc += total_ttc

        pdf.drawString(x + 350, y, f"{total_ht:.3f}")
        pdf.drawString(x + 450, y, f"{tva_obj.taux_tva:.3f} %")
        pdf.line(x, y - 5, width - 50, y - 5)
        y -= 20

        # Track TVA totals by rate
        rate = tva_obj.taux_tva
        if rate not in tva_totals:
            tva_totals[rate] = {'base': Decimal('0'), 'tva_amount': Decimal('0')}
        tva_totals[rate]['base'] += total_ht
        tva_totals[rate]['tva_amount'] += total_tva

    # Affichez le détail de la TVA par taux
    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    y -= 20

    for rate, amounts in tva_totals.items():
        pdf.drawString(x, y, f"Taux TVA {rate}%:")
        pdf.drawString(x + 150, y, f"Base: {amounts['base']:.3f}")
        pdf.drawString(x + 300, y, f"Mont. TVA : {amounts['tva_amount']:.3f}")
        y -= 20
    pdf.line(x, y+10 , width - 50, y+10 )
    y -= 20

    # Dessinez les totaux sur la dernière page
    if y < 100:  # Vérifiez s'il reste de l'espace pour les totaux
        draw_footer()
        pdf.showPage()
        page_number += 1
        y = height - 50
        draw_header()

    draw_totals()  # Affichez les totaux
    draw_footer()  # Dessinez le pied de page final

    pdf.showPage()
    pdf.save()

    return response

def get_article_data(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        data = {
            'prix_unitaire': article.prix_unitaire,
            'taux_tva': article.taux_tva,
        }
        return JsonResponse(data)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)




logger = logging.getLogger(__name__)

def create_devis(request):
    if request.method == 'POST':
        data = request.POST.copy()

        # Set the total number of forms for the formset
        data['form-TOTAL_FORMS'] = data.getlist('form-TOTAL_FORMS')[0]

        form = DevisForm(data)  # Use DevisForm instead of FactureForm
        formset = LigneDevisFormSet(data)  # Use LigneDevisFormSet instead of LigneFactureFormSet

        # Validate both the main form and the formset
        if form.is_valid() and formset.is_valid():
            devis = form.save(commit=False)

            # Retrieve the last Devis object by ordering by ID in descending order
            last_devis = Devis.objects.order_by('-id').first()

            if last_devis and last_devis.numero_devis.startswith("DVS-"):
                # Extract the numeric part after 'DVS-'
                last_number = int(last_devis.numero_devis.split('-')[1])
                # Increment the number and format without zero-padding
                new_number = last_number + 1
                devis.numero_devis = f"DVS-{new_number:04d}"
            else:
                # Start from DVS-1 if no last_devis found
                devis.numero_devis = "DVS-0001"

            devis.save()  # Save the devis instance

            # Associate each LigneDevis with the saved devis
            for ligne_form in formset:
                ligne = ligne_form.save(commit=False)
                ligne.devis = devis  # Associate the line item with the devis
                ligne.save()  # Save the line item (LigneDevis)

            messages.success(request, 'Quote created successfully!')
            return redirect('list_devis')  # Redirect to the quote list view (adjust the URL name as needed)
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = DevisForm()  # Use DevisForm instead of FactureForm
        formset = LigneDevisFormSet(queryset=LigneDevis.objects.none())  # Use LigneDevisFormSet instead of LigneFactureFormSet

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'devis/create_devis.html', context)  # Render a template for creating quotes

def list_devis(request):
    devis = Devis.objects.all().order_by("-created_at")  # Fetch all invoices
    module_actif = 'Gestion des Devis'  # Module actif à passer au template

    return render(request, 'devis/list_devis.html', {'devis': devis, 'module_actif': module_actif})

def get_prix_unitaire(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        return JsonResponse({"prix_unitaire": article.prix_unitaire})
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)

def get_taux_tva(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        return JsonResponse({"taux_tva": article.tva.taux_tva})
    except Article.DoesNotExist:
        return JsonResponse({"error": "Article not found"}, status=404)


def generate_devis_number():
    # Replace this logic with your own for generating unique invoice numbers
    last_devis = Devis.objects.order_by('id').last()
    if last_devis:
        return f"FCT-{last_devis.id + 1}"
    return "FCT-0001"  # First invoice



def delete_devis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)

    if request.method == 'POST':
        devis.delete()
        messages.success(request, f'La devis {devis.numero_devis} a été supprimée avec succès.')
        return redirect('list_devis')

    return render(request, 'devis/confirm_delete.html', {'devis': devis})



def afficher_devis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)
    lignes = devis.lignes_devis.all()  # Récupère les lignes associées à cette devis


    for ligne in lignes:
        print(
            f"Article: {ligne.article}, "
            f"Quantité: {ligne.quantite}, "
            f"Prix Unitaire: {ligne.prix_unitaire}, "
            f"Taux Remise: {ligne.taux_remise}, "
            f"Montant HT: {ligne.montant_ht}, "
            f"Montant TVA: {ligne.montant_tva}, "
            f"Montant TTC: {ligne.montant_ttc}"
        )

        
    context = {
        'devis': devis,
        'lignes': lignes,
    }
    return render(request, 'devis/afficher_devis.html', context)



def safe_decimal(value, default='0'):
    """Convertit en Decimal en retournant une valeur par défaut en cas d'erreur."""
    if value in [None, '']:  # Vérifie si la valeur est vide
        return Decimal(default)
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)

def modifier_devis(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)
    lignes_devis = devis.lignes_devis.all()

    if request.method == 'POST':
        form = DevisForm(request.POST, instance=devis)

        if form.is_valid():
            devis = form.save()

            # Process existing and new lines
            total_lines = max(
                int(key.split('-')[1]) + 1 for key in request.POST.keys() 
                if key.startswith('form-') and '-article' in key
            )

            lignes_gardees = set()

            # Iterate over all lines submitted in the form
            for i in range(total_lines):
                ligne_id = request.POST.get(f'form-{i}-id')
                delete_flag = request.POST.get(f'form-{i}-DELETE', 'off')

                if delete_flag == 'on' and ligne_id:
                    LigneDevis.objects.filter(id=ligne_id).delete()
                    continue  # Skip further processing of this line

                article_id = request.POST.get(f'form-{i}-article')
                quantite = request.POST.get(f'form-{i}-quantite', 0)
                taux_remise_value = safe_decimal(request.POST.get(f'form-{i}-taux_remise'), '0')
                prix_unitaire = safe_decimal(request.POST.get(f'form-{i}-prix_unitaire'), '0')

                if article_id:
                    if ligne_id:
                        ligne = LigneDevis.objects.filter(id=ligne_id).first()
                    else:
                        ligne = LigneDevis(devis=devis)

                    # Update or create the line
                    ligne.article_id = article_id
                    ligne.quantite = int(quantite)
                    ligne.taux_remise = taux_remise_value
                    ligne.prix_unitaire = prix_unitaire

                    # Calculate amounts
                    ligne.montant_ht = ligne.quantite * ligne.prix_unitaire * (1 - ligne.taux_remise / 100)
                    article = Article.objects.get(id=article_id)
                    ligne.ttva = safe_decimal(article.tva.taux_tva, '0')
                    ligne.montant_tva = ligne.montant_ht * ligne.ttva / 100
                    ligne.montant_ttc = ligne.montant_ht + ligne.montant_tva

                    ligne.save()
                    lignes_gardees.add(ligne.id)

            messages.success(request, 'Devis modifiée avec succès !')
            return redirect('list_devis')
        else:
            messages.error(request, 'Veuillez corriger les erreurs.')

    else:
        form = DevisForm(instance=devis)

    articles = Article.objects.select_related('tva').all()
    context = {
        'form': form,
        'devis': devis,
        'lignes_devis': lignes_devis,
        'articles': articles,
    }
    return render(request, 'devis/modifier_devis.html', context)



from django.shortcuts import get_object_or_404, redirect
import re

def transferer_devis_en_facture(request, devis_id):
    # Récupérer le devis
    devis = get_object_or_404(Devis, id=devis_id)
    
    # Trouver la dernière facture avec un numéro commençant par "FCT-"
    last_facture = Facture.objects.filter(numero_facture__startswith="FCT-").order_by('-numero_facture').first()
    
    if last_facture:
        # Extraire la partie numérique après "FCT-"
        match = re.search(r"FCT-(\d+)", last_facture.numero_facture)
        if match:
            last_number = int(match.group(1))
            # Incrémenter et formater le numéro
            new_number = last_number + 1
            numero_facture = f"FCT-{new_number:04d}"  # Formaté avec 4 chiffres
        else:
            # Par défaut, retourner FCT-1 si le format est incorrect
            numero_facture = "FCT-0001"
    else:
        # Aucun numéro existant, commencer par FCT-1
        numero_facture = "FCT-0001"

    # Créer une nouvelle facture basée sur le devis
    facture = Facture.objects.create(
        numero_facture=numero_facture,
        client=devis.client,
        date_facture=devis.date_devis,  # ou utilisez la date actuelle
        total_ht=devis.total_ht,
        total_tva=devis.total_tva,
        total_ttc=devis.total_ttc,
        # Copiez d'autres champs pertinents du devis
    )

    # Transférer les lignes de devis vers les lignes de facture
    for ligne_devis in devis.lignes_devis.all():
        facture.lignes_facture.create(
            article=ligne_devis.article,
            quantite=ligne_devis.quantite,
            prix_unitaire=ligne_devis.prix_unitaire,
            taux_remise=ligne_devis.taux_remise,
            # Ajoutez d'autres champs nécessaires
        )
    
    # Une fois la facture créée, rediriger vers la liste des devis
    return redirect('list_devis')





from django.http import JsonResponse

def delete_deviss(request):
    if request.method == 'POST':
        selected_ids = request.POST.get('selected_devis', '')  # Récupérer les IDs
        if selected_ids:
            selected_ids_list = [int(id) for id in selected_ids.split(',')]
            print(f"Devis sélectionnés pour suppression (avant suppression) : {selected_ids_list}")  # Log des IDs reçus
            
            # Supprimer les devis sélectionnés
            devis_deleted, deleted_objects = Devis.objects.filter(id__in=selected_ids_list).delete()
            
            # Obtenir le nombre de devis supprimés
            devis_count = deleted_objects.get('devis.Devis', 0)
            
            if devis_count > 0:
                # Retourner une réponse indiquant que la suppression a réussi
                return JsonResponse({'status': 'success', 'message': f'{devis_count} devis supprimés avec succès.'})
            else:
                return JsonResponse({'status': 'warning', 'message': "Aucun devis trouvé à supprimer."})
        else:
            return JsonResponse({'status': 'warning', 'message': "Aucun devis sélectionné."})
    
    return JsonResponse({'status': 'error', 'message': "Méthode non autorisée."})




def print_deviss(request):
    # Récupérer les devis sélectionnés depuis la requête
    devis_ids = request.POST.getlist('devis_ids')
    print(devis_ids)

    if not devis_ids:
        return HttpResponse("Aucun devis sélectionné", status=400)

    # Si les devis sont envoyés sous forme d'une seule chaîne de caractères séparée par des virgules
    devis_ids = devis_ids[0].split(',')

    # Convertir chaque ID en entier
    devis_ids = [int(devis_id.strip()) for devis_id in devis_ids]

    # Afficher les IDs pour vérifier qu'ils sont bien traités
    print(devis_ids)

    # Appeler la fonction generate_deviss_pdf avec les identifiants des devis
    return generate_devis_pdf1(devis_ids)


def generate_devis_pdf1(devis_ids):
    print(f"devis_ids before passing: {devis_ids}")

    # Créer la réponse HTTP avec un en-tête PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="devis_selectionnes.pdf"'

    # Créer le canvas PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    x = 50
    initial_y = height - 50  # Position initiale pour le contenu

    def draw_header():
        nonlocal y
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(x, y, "Mohsen GHARBI GAMMOUDA Services")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, y - 20, "20 Av. Habib Bourguiba, Sidi Bouzid")
        pdf.drawString(x, y - 40, "Tel: 76 625 788 - 98 417 237")
        pdf.drawString(x, y - 60, "Email: gmohsen6@gmail.com")
        pdf.drawString(x, y - 80, "MF: 0421452S")
        pdf.drawString(x, y - 100, "RIB: 4663")
        y -= 160

    def draw_footer(page_number):
        pdf.setFont("Helvetica", 10)
        pdf.drawString(width - 100, 30, f"Page {page_number}")

    def draw_totals(total_ht, total_tva, total_ttc):
        nonlocal y
        pdf.setFont("Helvetica-Bold", 12)
        y -= 10
        pdf.drawString(x + 300, y, "Total HT:")
        pdf.drawString(x + 370, y, f"{total_ht:.3f}")
        y -= 20
        pdf.drawString(x + 300, y, "Total TVA:")
        pdf.drawString(x + 370, y, f"{total_tva:.3f}")
        y -= 20
        pdf.drawString(x + 300, y, "Total TTC:")
        pdf.drawString(x + 370, y, f"{total_ttc:.3f}")

    page_number = 1

    for index, devis_id in enumerate(devis_ids):
        # Réinitialiser y pour chaque devis
        y = initial_y
        devis = get_object_or_404(Devis, id=devis_id)  # Replace Facture with Devis model
        ligne_devis = devis.lignes_devis.all()  # Replace lignes_facture with lignes_devis

        tva_totals = {}

        # Si ce n'est pas le premier devis, passer à une nouvelle page
        if index > 0:
            pdf.showPage()
            page_number += 1

        # Dessiner l'entête pour chaque devis
        draw_header()
        pdf.drawString(x, y, f"Devis No: {devis.numero_devis}")
        pdf.drawString(x, y - 20, f"Date: {devis.date_devis.strftime('%d/%m/%Y')}")
        pdf.drawString(x, y - 40, f"Client: {devis.client}")
        y -= 80

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Article")
        pdf.drawString(x + 150, y, "Qté")
        pdf.drawString(x + 220, y, "P.U")
        pdf.drawString(x + 300, y, "Rem %")
        pdf.drawString(x + 350, y, "Net. HT")
        pdf.drawString(x + 450, y, "TVA %")
        pdf.line(x, y - 5, width - 50, y - 5)
        y -= 25

        pdf.setFont("Helvetica", 8)

        total_ht, total_tva, total_ttc = Decimal('0'), Decimal('0'), Decimal('0')

        for ligne in ligne_devis:
            if y < 50:  # Si l'espace restant est insuffisant pour afficher une ligne
                draw_footer(page_number)
                pdf.showPage()
                page_number += 1
                y = initial_y
                draw_header()

            pdf.drawString(x, y, str(ligne.article))
            pdf.drawString(x + 150, y, str(ligne.quantite))
            pdf.drawString(x + 220, y, f"{ligne.prix_unitaire:.3f}")
            pdf.drawString(x + 300, y, f"{ligne.taux_remise:.2f}%")
            net_ht = ligne.quantite * ligne.prix_unitaire * (1 - ligne.taux_remise / 100)
            total_ht += net_ht

            tva_obj = ligne.article.tva
            tva_amount = net_ht * tva_obj.taux_tva / 100
            total_tva += tva_amount
            total_ttc += net_ht + tva_amount

            pdf.drawString(x + 350, y, f"{net_ht:.3f}")
            pdf.drawString(x + 450, y, f"{tva_obj.taux_tva:.2f}%")
            y -= 20

            # Ajouter les totaux TVA par taux
            rate = tva_obj.taux_tva
            if rate not in tva_totals:
                tva_totals[rate] = {'base': Decimal('0'), 'tva_amount': Decimal('0')}
            tva_totals[rate]['base'] += net_ht
            tva_totals[rate]['tva_amount'] += tva_amount

        if y < 50:  # Changer de page si nécessaire
            draw_footer(page_number)
            pdf.showPage()
            page_number += 1
            y = initial_y
            draw_header()

        pdf.setFont("Helvetica-Bold", 12)
        y -= 20
        for rate, amounts in tva_totals.items():
            pdf.drawString(x, y, f"TVA {rate}%:")
            pdf.drawString(x + 150, y, f"Base: {amounts['base']:.3f}")
            pdf.drawString(x + 300, y, f"Mont. TVA: {amounts['tva_amount']:.3f}")
            y -= 20

        # Affichage des totaux généraux pour le devis
        draw_totals(total_ht, total_tva, total_ttc)

    # Finaliser le PDF
    pdf.save()
    return response



def devis_list_rechMultc(request):
    devis = Devis.objects.all()
    
    # Vérifier si la recherche multicritère est demandée
    show_search = request.GET.get('show_search', False)
    
    # Ajouter une logique pour filtrer les devis si nécessaire
    field = request.GET.get('field', '')
    operator = request.GET.get('operator', '')
    value = request.GET.get('value', '')
    range_min = request.GET.get('range_min', None)
    range_max = request.GET.get('range_max', None)

    if field and operator and value:
        if operator == 'exact':
            devis = devis.filter(**{f'{field}__exact': value})
        elif operator == 'icontains':
            devis = devis.filter(**{f'{field}__icontains': value})
        elif operator == 'gt':
            devis = devis.filter(**{f'{field}__gt': value})
        elif operator == 'lt':
            devis = devis.filter(**{f'{field}__lt': value})
        elif operator == 'neq':
            devis = devis.exclude(**{f'{field}__exact': value})
        elif operator == 'lte':
            devis = devis.filter(**{f'{field}__lte': value})
        elif operator == 'gte':
            devis = devis.filter(**{f'{field}__gte': value})
        elif operator == 'range' and range_min and range_max:
            devis = devis.filter(**{f'{field}__range': (range_min, range_max)})

    return render(request, 'devis/list_devis.html', {'devis': devis, 'show_search': show_search})
