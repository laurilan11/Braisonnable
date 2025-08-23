from .models import Reservation
from django.core.exceptions import ValidationError
import datetime
from datetime import time
from django import forms
from django.db.models import Sum

MAX_PERSONNES = 6

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'email', 'telephone', 'nombre_personnes', 'date', 'heure', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'heure': forms.TimeInput(attrs={'type': 'time', 'min': '12:00', 'max': '23:00', 'step': 1800}),  # 15 min step
        }

    def clean_nombre_personnes(self):
        nombre = self.cleaned_data['nombre_personnes']
        if nombre < 1 or nombre > 6:
            raise ValidationError("Le nombre de personnes doit être compris entre 1 et 6.")
        return nombre

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise ValidationError("La date n'est pas valide.")
        return date

    def clean_heure(self):
        heure = self.cleaned_data.get('heure')
        if not (time(12, 0) <= heure <= time(23, 0)):
            raise forms.ValidationError("L'heure doit être comprise entre 12h00 et 23h00.")
        if heure.minute % 30 != 0:
            raise forms.ValidationError("L'heure doit être un multiple de 30 minutes.")
        return heure

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        heure = cleaned_data.get("heure")
        personnes = cleaned_data.get("nombre_personnes")

        if date and heure and personnes:
            total = (
                    Reservation.objects
                    .filter(date=date, heure=heure)
                    .aggregate(total=Sum("nombre_personnes"))["total"] or 0
            )

            if total + personnes > MAX_PERSONNES:
                raise forms.ValidationError("Ce créneau est déjà complet. Veuillez en choisir un autre.")
