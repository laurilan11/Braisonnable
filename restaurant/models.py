from django.db import models

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.nom

class Reservation(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True, null=True)
    nombre_personnes = models.PositiveSmallIntegerField()
    date = models.DateField()
    heure = models.TimeField()
    message = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, default='En attente')  # statut de la réservation
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Réservation de {self.nom} pour {self.nombre_personnes} pers. le {self.date} à {self.heure}"
