from django.contrib import admin
from .models import Reservation  # adapte selon le nom de ton modèle

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date', 'heure', 'nombre_personnes', 'statut')
    list_filter = ('date', 'statut')
    search_fields = ('nom', 'email', 'telephone')
    ordering = ('date', 'heure')
    #readonly_fields = ('created_at', 'updated_at')  # si tu as ces champs

    # Optionnel : pour personnaliser le formulaire admin
    fieldsets = (
        (None, {
            'fields': ('nom', 'email', 'telephone', 'nombre_personnes', 'date', 'heure', 'message', 'statut')
        }),
        ('Informations supplémentaires', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

