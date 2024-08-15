from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


#Model Hotel

class Hotel(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model().objects.first().pk)
    nom = models.CharField(max_length=300)
    description = models.TextField(max_length=5000)
    statut = models.IntegerField(choices=((1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')), default=0)
    adresse = models.CharField(max_length=355)
    ville = models.CharField(max_length=150)
    pays = models.CharField(max_length=150)
    coordonnees_tel = models.CharField(max_length=20)
    nombre_de_chambres = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='hotel_photos/', blank=True, null=True)
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
    
    def afficher_etoiles(self):
        return "⭐" * self.statut

#Model Photo d'hôtel
class Photo(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f"Photo de {self.hotel.nom}"
    
    
#Model Chambre    
class Chambre(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model().objects.first().pk)
    TYPE_CHAMBRE_CHOICES = (
        ('simple', 'Simple'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )

    ETAGE_CHOICES = (
        (1, '1er étage'),
        (2, '2ème étage'),
        (3, '3ème étage'),
        (4, '4ème étage'),
        (5, '5ème étage'),
    )

    VUE_SUR_MER_CHOICES = (
        ('oui', 'Oui'),
        ('non', 'Non'),
    )

    nom = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    hotel = models.ForeignKey(Hotel, related_name='chambres', on_delete=models.CASCADE)
    type_de_chambre = models.CharField(max_length=20, choices=TYPE_CHAMBRE_CHOICES)
    surface = models.DecimalField(max_digits=5, decimal_places=2)  # En mètres carrés
    tarif_reservation_par_jour = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tarif_par_nuit = models.DecimalField(max_digits=10, decimal_places=2)
    vue_sur_mer = models.CharField(max_length=3, choices=VUE_SUR_MER_CHOICES, blank=True, null=True, default=('non', 'Non'))
    emplacement = models.IntegerField(choices=ETAGE_CHOICES)
    photo = models.ImageField(upload_to='chambre_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.hotel.nom})"


#Model Photo de chambre
class PhotoChambre(models.Model):
    chambre = models.ForeignKey(Chambre, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chambre_images/')


#Model prestations d'hôtel
class PrestationHotel(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='prestations', on_delete=models.CASCADE)
    activites = models.JSONField(default=list, blank=True)
    services = models.JSONField(default=list, blank=True)
    reception_evenements = models.JSONField(default=list, blank=True)
    langues_personnel = models.JSONField(default=list, blank=True)
    methodes_paiement = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'Prestation Hotel {self.pk}'


# Model restaurant
class Restaurant(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model().objects.first().pk)
    nom = models.CharField(max_length=300)
    description = models.TextField(max_length=5000)
    statut = models.IntegerField(choices=((1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')), default=0)
    adresse = models.CharField(max_length=355)
    ville = models.CharField(max_length=150)
    pays = models.CharField(max_length=150)
    coordonnees_tel = models.CharField(max_length=20)
    nombre_de_tables = models.PositiveIntegerField(default=0)
    prix_reservation = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    photo = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
    
    def afficher_etoiles(self):
        return "⭐" * self.statut


#Model Photo Restaurant
class PhotoRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')

    def __str__(self):
        return f"Photo de {self.hotel.nom}"
    
    
#Model Menu
class Menu(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model().objects.first().pk)
    # types de plats
    TYPE_PLAT_CHOICES = [
        ('entrée', 'Entrée'),
        ('plat principal', 'Plat Principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
    ]
    
    nom = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)
    type_de_plat = models.CharField(max_length=20, choices=TYPE_PLAT_CHOICES)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    photo = models.ImageField(upload_to='menus_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.restaurant.nom})"


class PhotoMenu(models.Model):
    menu = models.ForeignKey(Menu, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_images/')



#Model prestations de restaurant
class PrestationRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='prestations', on_delete=models.CASCADE)
    services = models.JSONField(default=list, blank=True)
    types_de_cuisine = models.JSONField(default=list, blank=True)
    langues_personnel = models.JSONField(default=list, blank=True)
    methodes_paiement = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'Prestation Restaurant {self.pk}'

#valider le type de ficher document gerant
def validate_file_type(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Type de fichier non supporté. Les types supportés sont : {", ".join(valid_extensions)}')

#Model gerant
class Gerant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model().objects.first().pk)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=300)
    pays = models.CharField(max_length=70)
    coordonnees_tel = models.CharField(max_length=20)
    adresse = models.CharField(max_length=350)
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class DocumentGerant(models.Model):
    gerant = models.ForeignKey(Gerant, related_name='documents', on_delete=models.CASCADE)
    document = models.FileField(upload_to='gerant_documents/', validators=[validate_file_type], blank=True, null=True)



class ReservationChambre(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date_arrivee = models.DateField()
    nombre_personnes = models.PositiveIntegerField()
    date_reservation = models.DateTimeField(default=timezone.now)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numero_confirmation = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_confirmer = models.BooleanField(default=False)
    statut_paiement = models.BooleanField(default=False)
    validation = models.CharField(max_length=50, default='En cours de validation')
    

class ReservationRestaurant(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_arrivee = models.DateField()
    heure_arrivee = models.TimeField()
    nombre_personnes = models.PositiveIntegerField()
    date_reservation = models.DateTimeField(default=timezone.now)
    numero_confirmation = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_confirmer = models.BooleanField(default=False)
    statut_paiement = models.BooleanField(default=False)
    validation = models.CharField(max_length=50, default='En cours de validation')
    

class ReservationRestaurantPaiement(models.Model):
    reservation = models.ForeignKey(ReservationRestaurant, on_delete=models.CASCADE)
    votre_numero_telephone = models.CharField(max_length=20)
    numero_telephone_destinataire = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    

class ReservationHotelPaiement(models.Model):
    reservation = models.ForeignKey(ReservationChambre, on_delete=models.CASCADE)
    votre_numero_telephone = models.CharField(max_length=20)
    numero_telephone_destinataire = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=10, decimal_places=0, default=0)