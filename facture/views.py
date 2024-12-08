from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, TVA, Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet  # Ensure you have this import
from client.models import Client
from article.models import Article
from django.http import JsonResponse
from django.utils import timezone
import logging
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from decimal import Decimal, InvalidOperation




from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.utils import simpleSplit

def generate_facture_pdf(request, facture_id):
    # Create the HttpResponse object with the PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture_id}.pdf"'

    # Create the PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Get the invoice and associated lines
    facture = get_object_or_404(Facture, id=facture_id)
    ligne_factures = facture.lignes_facture.all()  # Use the new related_name

    # Initialize position, page number
    x = 50
    y = height - 50
    page_number = 1

    # Header function
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

    # Footer function with page number
    def draw_footer():
        pdf.setFont("Helvetica", 10)
        pdf.drawString(width - 100, 30, f"Page {page_number}")

    # Totals function
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

    # Start first page
    draw_header()
    pdf.drawString(x, y, f"Facture No: {facture.numero_facture}")
    pdf.drawString(x, y - 20, f"Date: {facture.date_facture.strftime('%d/%m/%Y')}")
    pdf.drawString(x, y - 40, f"Client: {facture.client}")
    y -= 80

    # Table header
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

    # Initialize totals
    total_general_ht = Decimal('0')
    total_general_tva = Decimal('0')
    total_general_ttc = Decimal('0')
    tva_totals = {}

    # Add article lines
    for ligne in ligne_factures:
        if y < 50:
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

        # Handle multiline text for article description
        article_text = str(ligne.article)
        max_width = 150  # Adjust width for wrapping text
        wrapped_text = simpleSplit(article_text, "Helvetica", 8, max_width)

        # Draw article text on multiple lines
        for line in wrapped_text:
            pdf.drawString(x, y, line)
            y -= 15

        pdf.drawString(x + 150, y, str(ligne.quantite))
        pdf.drawString(x + 220, y, f"{ligne.prix_unitaire:.3f}")
        pdf.drawString(x + 300, y, f"{ligne.taux_remise:.3f} %")


        # Calculate amounts
        total_ht = ligne.quantite * ligne.prix_unitaire * (1 - ligne.taux_remise / 100)
        tva_obj = get_object_or_404(TVA, id=ligne.article.tva_id)
        total_tva = total_ht * (tva_obj.taux_tva / 100)
        total_general_ht += total_ht
        total_general_tva += total_tva
        total_ttc = total_ht + total_tva
        total_general_ttc += total_ttc

        pdf.drawRightString(x + 400, y, f"{total_ht:.3f}")
        pdf.drawString(x + 450, y, f"{tva_obj.taux_tva:.3f} %")
        pdf.line(x, y - 5, width - 50, y - 5)
        y -= 20

        # Track TVA totals by rate
        rate = tva_obj.taux_tva
        if rate not in tva_totals:
            tva_totals[rate] = {'base': Decimal('0'), 'tva_amount': Decimal('0')}
        tva_totals[rate]['base'] += total_ht
        tva_totals[rate]['tva_amount'] += total_tva

    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    y -= 20 
    for rate, amounts in tva_totals.items():
        pdf.drawString(x, y, f"TVA {rate}%:")
        pdf.drawString(x + 150, y, f"Base: {amounts['base']:.3f}")
        pdf.drawString(x + 300, y, f"Mont. TVA : {amounts['tva_amount']:.3f}")
        y -= 20

    pdf.line(x, y + 10, width - 50, y + 10)
    y -= 20

    if y < 100:
        draw_footer()
        pdf.showPage()
        page_number += 1
        y = height - 50
        draw_header()

    draw_totals()
    draw_footer()
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

from django.db.models import Max

from django.db.models import Max
import re


def create_facture(request):
    if request.method == 'POST':
        print("Submitted client:", request.POST.get("client"))  # Debugging the submitted client value

        data = request.POST.copy()

        # Ensure 'client' field is correctly set
        client_id = data.get("client")
        if not client_id:
            messages.error(request, "Client selection is required.")
        else:
            data["client"] = client_id

        # Set the total number of forms for the formset
        data['form-TOTAL_FORMS'] = data.getlist('form-TOTAL_FORMS')[0]

        form = FactureForm(data)
        formset = LigneFactureFormSet(data)

        # Validate both the main form and the formset
        if form.is_valid() and formset.is_valid():
            facture = form.save(commit=False)

            # Retrieve the last Facture object by ordering by numero_facture
            last_facture = Facture.objects.filter(numero_facture__startswith="FCT-").order_by('-numero_facture').first()

            if last_facture:
                # Extract the numeric part after 'FCT-' using regex
                import re
                match = re.search(r"FCT-(\d+)", last_facture.numero_facture)
                if match:
                    last_number = int(match.group(1))
                    # Increment the number and format it as required
                    new_number = last_number + 1
                    facture.numero_facture = f"FCT-{new_number:04d}"
                else:
                    # Default to FCT-1 if the format is not valid
                    facture.numero_facture = "FCT-0001"
            else:
                # Start from FCT-1 if no last_facture found
                facture.numero_facture = "FCT-0001"

            facture.save()  # Save the facture instance

            # Associate each LigneFacture with the saved facture
            for ligne_form in formset:
                ligne = ligne_form.save(commit=False)
                ligne.facture = facture  # Associate the line item with the facture
                ligne.save()  # Save the line item (LigneFacture)

            messages.success(request, 'Invoice created successfully!')
            return redirect('list_factures')  # Redirect to the invoice list view
        else:
            # Debug form errors
            print("FactureForm Errors:", form.errors)
            print("Formset Errors:", formset.errors)
            messages.error(request, 'Please correct the errors below.')

    else:
        form = FactureForm()
        formset = LigneFactureFormSet(queryset=LigneFacture.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'facture/create_facture.html', context)


def list_factures(request):
    factures = Facture.objects.all().order_by('-created_at')

    module_actif = 'Gestion des Factures'  # Module actif à passer au template

    return render(request, 'facture/list_factures.html', {'factures': factures, 'module_actif': module_actif})

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


def generate_facture_number():
    # Replace this logic with your own for generating unique invoice numbers
    last_facture = Facture.objects.order_by('id').last()
    if last_facture:
        return f"FCT-{last_facture.id + 1}"
    return "FCT-0001"  # First invoice



def delete_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    if request.method == 'POST':
        facture.delete()
        messages.success(request, f'La facture {facture.numero_facture} a été supprimée avec succès.')
        return redirect('list_factures')

    return render(request, 'facture/confirm_delete.html', {'facture': facture})



def afficher_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    lignes = facture.lignes_facture.all()  # Récupère les lignes associées à cette facture


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
        'facture': facture,
        'lignes': lignes,
    }
    return render(request, 'facture/afficher_facture.html', context)


def safe_decimal(value, default='0'):
    """Convertit en Decimal en retournant une valeur par défaut en cas d'erreur."""
    if value in [None, '']:  # Vérifie si la valeur est vide
        return Decimal(default)
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)

def modifier_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    lignes_facture = facture.lignes_facture.all()

    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)

        if form.is_valid():
            facture = form.save(commit=False)  # Ne pas sauvegarder immédiatement

            # Process existing and new lines first
            total_lines = max(
                int(key.split('-')[1]) + 1 for key in request.POST.keys() 
                if key.startswith('form-') and '-article' in key
            )

            lignes_gardees = set()

            for i in range(total_lines):
                ligne_id = request.POST.get(f'form-{i}-id')
                delete_flag = request.POST.get(f'form-{i}-DELETE', 'off')

                if delete_flag == 'on' and ligne_id:
                    LigneFacture.objects.filter(id=ligne_id).delete()
                    continue

                article_id = request.POST.get(f'form-{i}-article')
                quantite = request.POST.get(f'form-{i}-quantite', 0)
                taux_remise_value = safe_decimal(request.POST.get(f'form-{i}-taux_remise'), '0')
                prix_unitaire = safe_decimal(request.POST.get(f'form-{i}-prix_unitaire'), '0')

                if article_id:
                    ligne = LigneFacture.objects.filter(id=ligne_id).first() if ligne_id else LigneFacture(facture=facture)

                    ligne.article_id = article_id
                    ligne.quantite = int(quantite)
                    ligne.taux_remise = taux_remise_value
                    ligne.prix_unitaire = prix_unitaire
                    ligne.montant_ht = ligne.quantite * ligne.prix_unitaire * (1 - ligne.taux_remise / 100)

                    article = Article.objects.get(id=article_id)
                    ligne.ttva = safe_decimal(article.tva.taux_tva, '0')
                    ligne.montant_tva = ligne.montant_ht * ligne.ttva / 100
                    ligne.montant_ttc = ligne.montant_ht + ligne.montant_tva
                    ligne.save()

                    lignes_gardees.add(ligne.id)

            # Recalcul des totaux après avoir traité les lignes
            total_ht = sum(ligne.montant_ht for ligne in facture.lignes_facture.all())
            total_tva = sum(ligne.montant_tva for ligne in facture.lignes_facture.all())
            total_ttc = total_ht + total_tva

            facture.total_ht = total_ht
            facture.total_tva = total_tva
            facture.total_ttc = total_ttc

            # Sauvegarder la facture avec les totaux calculés
            facture.save()

            messages.success(request, 'Facture modifiée avec succès !')
            return redirect('list_factures')
        else:
            print("Erreurs du formulaire Facture:", form.errors)
            messages.error(request, 'Veuillez corriger les erreurs.')
    else:
        form = FactureForm(instance=facture)

    articles = Article.objects.select_related('tva').all()
    context = {
        'form': form,
        'facture': facture,
        'lignes_facture': lignes_facture,
        'articles': articles,
    }
    return render(request, 'facture/modifier_facture.html', context)







def delete_factures(request):
    if request.method == 'POST':
        selected_ids = request.POST.get('selected_factures', '')  # Récupérer les IDs
        if selected_ids:
            selected_ids_list = [int(id) for id in selected_ids.split(',')]
            print(f"Factures sélectionnées pour suppression (avant suppression) : {selected_ids_list}")  # Log des IDs reçus
            
            # Suppression des factures sélectionnées
            factures_deleted, deleted_objects = Facture.objects.filter(id__in=selected_ids_list).delete()
            
            # Obtenir uniquement le nombre de factures supprimées
            factures_count = deleted_objects.get('facture.Facture', 0)
            
            if factures_count > 0:
                # Retourner le nombre de factures supprimées dans la réponse
                return JsonResponse({'status': 'success', 'message': f'{factures_count} factures supprimées avec succès.'})
            else:
                return JsonResponse({'status': 'warning', 'message': "Aucune facture trouvée à supprimer."})
        else:
            return JsonResponse({'status': 'warning', 'message': "Aucune facture sélectionnée."})
    
    return JsonResponse({'status': 'error', 'message': "Méthode non autorisée."})

    
def print_factures(request):
    if request.method == "POST":
        facture_ids = request.POST.get('facture_ids', '')

        if not facture_ids:
            return JsonResponse({"status": "error", "message": "Aucun ID de facture sélectionné"}, status=400)

        facture_ids = [int(id.strip()) for id in facture_ids.split(',') if id.isdigit()]

        print("IDs des factures reçus sur le serveur :", facture_ids)

        return generate_factures_pdf1(facture_ids)

    return JsonResponse({"status": "error", "message": "Requête incorrecte"}, status=400)


def generate_factures_pdf1(facture_ids):
    print(f"facture_ids before passing: {facture_ids}")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factures_selectionnees.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    x = 50
    initial_y = height - 50

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

    for index, facture_id in enumerate(facture_ids):
        y = initial_y
        facture = get_object_or_404(Facture, id=facture_id)
        ligne_factures = facture.lignes_facture.all()

        tva_totals = {}

        if index > 0:
            pdf.showPage()
            page_number += 1

        draw_header()
        pdf.drawString(x, y, f"Facture No: {facture.numero_facture}")
        pdf.drawString(x, y - 20, f"Date: {facture.date_facture.strftime('%d/%m/%Y')}")
        pdf.drawString(x, y - 40, f"Client: {facture.client}")
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

        for ligne in ligne_factures:
            if y < 50:
                draw_footer(page_number)
                pdf.showPage()
                page_number += 1
                y = initial_y
                draw_header()

            article_text = str(ligne.article)
            wrapped_text = simpleSplit(article_text, "Helvetica", 8, width - x - 450)

            for line in wrapped_text:
                pdf.drawString(x, y, line)
                y -= 12

            pdf.drawString(x + 150, y, str(ligne.quantite))
            pdf.drawString(x + 220, y, f"{ligne.prix_unitaire:.3f}")
            pdf.drawString(x + 300, y, f"{ligne.taux_remise:.2f}%")

            pdf.line(x, y - 5, width - 50, y - 5)


            net_ht = ligne.quantite * ligne.prix_unitaire * (1 - ligne.taux_remise / 100)
            total_ht += net_ht

            tva_obj = ligne.article.tva
            tva_amount = net_ht * tva_obj.taux_tva / 100
            total_tva += tva_amount
            total_ttc += net_ht + tva_amount

            pdf.drawString(x + 350, y, f"{net_ht:.3f}")
            pdf.drawString(x + 450, y, f"{tva_obj.taux_tva:.2f}%")
            y -= 20

            rate = tva_obj.taux_tva
            if rate not in tva_totals:
                tva_totals[rate] = {'base': Decimal('0'), 'tva_amount': Decimal('0')}
            tva_totals[rate]['base'] += net_ht
            tva_totals[rate]['tva_amount'] += tva_amount

        if y < 50:
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
            pdf.line(x, y - 2, width - 50, y - 2)

            y -= 20

        draw_totals(total_ht, total_tva, total_ttc)

    pdf.save()
    return response



from datetime import datetime
from django.db.models import Q
from django.shortcuts import render
from .models import Facture

from datetime import datetime
from django.db.models import Q
from django.shortcuts import render
from .models import Facture

def list_facture_rechMultc(request):
    factures = Facture.objects.all().order_by("-created_at")

    # Récupération des paramètres de recherche
    show_search = request.GET.get('show_search', False)
    field = request.GET.get('field', '')
    operator = request.GET.get('operator', '')
    value = request.GET.get('value', '')
    field2 = request.GET.get('field2', '')
    operator2 = request.GET.get('operator2', '')
    value2 = request.GET.get('value2', '')
    logical_operator = request.GET.get('logical_operator', 'and')  # Par défaut 'and'

    # Initialisation des filtres
    query1 = Q()
    query2 = Q()

    # Fonction utilitaire pour convertir une date au format français
    def convert_french_date(date_str):
        try:
            return datetime.strptime(date_str, '%d/%m/%Y').date()
        except ValueError:
            return None  # Retourne None si le format est invalide

    # Fonction utilitaire pour construire les Q objects
    def construct_query(field, operator, value):
        if operator == 'exact':
            return Q(**{f"{field}__exact": value})
        elif operator == 'icontains':
            return Q(**{f"{field}__icontains": value})
        elif operator == 'gt':
            return Q(**{f"{field}__gt": value})
        elif operator == 'lt':
            return Q(**{f"{field}__lt": value})
        elif operator == 'gte':
            return Q(**{f"{field}__gte": value})
        elif operator == 'lte':
            return Q(**{f"{field}__lte": value})
        return Q()  # Retourne un Q vide si l'opérateur est invalide

    # Adapter les noms de champs pour inclure les relations
    def adjust_field_name(field):
        if field == 'compte':  # Champ `compte` se trouve dans le modèle Client
            return 'client__compte'
        return field  # Aucun changement pour les autres champs

    # Ajustement des noms de champs
    field = adjust_field_name(field)
    field2 = adjust_field_name(field2)

    # Construction du premier critère
    if field and operator and value:
        if field == 'date_facture':  # Conversion nécessaire pour les dates
            date_value = convert_french_date(value)
            if date_value:
                query1 = construct_query(field, operator, date_value)
        else:
            query1 = construct_query(field, operator, value)

    # Construction du deuxième critère
    if field2 and operator2 and value2:
        if field2 == 'date_facture':  # Conversion nécessaire pour les dates
            date_value2 = convert_french_date(value2)
            if date_value2:
                query2 = construct_query(field2, operator2, date_value2)
        else:
            query2 = construct_query(field2, operator2, value2)

    # Combinaison des deux critères avec l'opérateur logique
    if logical_operator == 'and':
        final_query = query1 & query2
    elif logical_operator == 'or':
        final_query = query1 | query2
    else:
        final_query = query1  # Si opérateur logique invalide

    # Appliquer le filtre final
    factures = factures.filter(final_query)

    # Contexte pour le rendu
    context = {
        'factures': factures,
        'show_search': show_search,
    }
    return render(request, 'facture/list_factures.html', context)
