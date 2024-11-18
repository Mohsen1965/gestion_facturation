from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, TVA, Facture, LigneFacture
from .forms import FactureForm, LigneFactureFormSet  # Ensure you have this import
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

from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from decimal import Decimal
from facture.models import Facture
from tva.models import TVA

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

        pdf.drawString(x, y, str(ligne.article))
        pdf.drawString(x + 150, y, str(ligne.quantite))
        pdf.drawString(x + 220, y, f"{ligne.prix_unitaire:.3f}")
        pdf.drawString(x + 300, y, f"{ligne.taux_remise:.3f} %")

        # Calculate amounts
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

    # Display TVA by rate
    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "TVA Breakdown by Rate")
    y -= 20

    for rate, amounts in tva_totals.items():
        pdf.drawString(x, y, f"Taux TVA {rate}%:")
        pdf.drawString(x + 150, y, f"Base: {amounts['base']:.3f}")
        pdf.drawString(x + 300, y, f"Mont. TVA : {amounts['tva_amount']:.3f}")
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
        data = request.POST.copy()

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
                    facture.numero_facture = "FCT-1"
            else:
                # Start from FCT-1 if no last_facture found
                facture.numero_facture = "FCT-1"

            facture.save()  # Save the facture instance

            # Associate each LigneFacture with the saved facture
            for ligne_form in formset:
                ligne = ligne_form.save(commit=False)
                ligne.facture = facture  # Associate the line item with the facture
                ligne.save()  # Save the line item (LigneFacture)

            messages.success(request, 'Invoice created successfully!')
            return redirect('list_factures')  # Redirect to the invoice list view
        else:
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
    factures = Facture.objects.all()  # Fetch all invoices
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
    return "FCT-1"  # First invoice



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
            facture = form.save()

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
                    LigneFacture.objects.filter(id=ligne_id).delete()
                    continue  # Skip further processing of this line

                article_id = request.POST.get(f'form-{i}-article')
                quantite = request.POST.get(f'form-{i}-quantite', 0)
                taux_remise_value = safe_decimal(request.POST.get(f'form-{i}-taux_remise'), '0')
                prix_unitaire = safe_decimal(request.POST.get(f'form-{i}-prix_unitaire'), '0')

                if article_id:
                    if ligne_id:
                        ligne = LigneFacture.objects.filter(id=ligne_id).first()
                    else:
                        ligne = LigneFacture(facture=facture)

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

            messages.success(request, 'Facture modifiée avec succès !')
            return redirect('list_factures')
        else:
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
        selected_ids = request.POST.get('selected_factures', '')  # Retrieve the string of IDs
        print("Factures sélectionnées :", selected_ids)  # Debugging

        if selected_ids:
            # Split the string into a list of integers
            selected_ids_list = [int(id) for id in selected_ids.split(',')]

            # Delete the selected factures
            Facture.objects.filter(id__in=selected_ids_list).delete()

            return JsonResponse({'status': 'success', 'message': f"{len(selected_ids_list)} facture(s) supprimée(s)."})
        else:
            return JsonResponse({'status': 'warning', 'message': "Aucune facture sélectionnée."})

    return JsonResponse({'status': 'error', 'message': "Méthode non autorisée."})
