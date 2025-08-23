from datetime import date

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ReservationForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import Reservation


def home(request):
    return render(request, 'restaurant/home.html')

def menu(request):
    return render(request, 'restaurant/menu.html')

from datetime import time, timedelta, datetime


def generate_time_slots(start_hour=12, end_hour=23, step_minutes=30):
    times = []
    current_time = datetime.combine(datetime.today(), time(start_hour, 0))
    end_time = datetime.combine(datetime.today(), time(end_hour, 0))
    while current_time <= end_time:
        times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=step_minutes)
    return times

def reservations(request):
    horaires = generate_time_slots()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            # Formatage de la date en JJ/MM/AAAA
            date_formatee = reservation.date.strftime("%d/%m/%Y")
            # Envoi mail confirmation
            send_mail(
                subject="Confirmation de votre réservation chez Braisonnable",
                message=(
                    f"Bonjour {reservation.nom},\n\n"
                    f"Votre réservation pour {reservation.nombre_personnes} personne(s) "
                    f"le {date_formatee} à {reservation.heure} a bien été enregistrée.\n\n"
                    "À bientôt chez Braisonnable !"
                ),
                from_email="gablauric@gmail.com",  # Remplace par ton email Gmail
                recipient_list=[reservation.email],
                fail_silently=False,
            )
            messages.success(request, "Votre réservation a été enregistrée. Un mail de confirmation vous a été envoyé.")
            return redirect('reservation_success')
    else:
        form = ReservationForm()
    return render(request, 'restaurant/reservations.html', {'form': form, "horaires": horaires,})


def reservation_success(request):
    return render(request, 'restaurant/reservation_success.html')

def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contenu = f"Nom : {nom}\nEmail : {email}\nMessage :\n{message}"

        send_mail(
            subject='Nouveau message de contact depuis le site',
            message=contenu,
            from_email=email,
            recipient_list=['gablauric@gmail.com'],
            fail_silently=False,
        )

        return HttpResponseRedirect(reverse('messageenvoye'))  # ou une page de confirmation

    return render(request, 'restaurant/contact.html')

def recrute(request):
    return render(request, 'restaurant/messageenvoye.html')

def about(request):
    return render(request, 'restaurant/about.html')
