from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Min, Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
import hashlib
from accounts.views import user_logged_in, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from datetime import datetime
# from django.template import loader


# Users

@user_logged_in
def accueil(request):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    
    hotels = Hotel.objects.all()
    hotels_with_min_price = []

    for hotel in hotels:
        min_price_chambre = Chambre.objects.filter(hotel=hotel).aggregate(
            Min("tarif_par_nuit")
        )
        min_price = min_price_chambre["tarif_par_nuit__min"]
        hotels_with_min_price.append({"hotel": hotel, "min_price": min_price})
        
        
    restaurants = Restaurant.objects.all()
    restaurants_with_min_price = []

    for restaurant in restaurants:
        # Filtre les menus par type "plat principal" et calcule le prix minimum
        min_price_menu = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).aggregate(min_prix=Min("prix"))
        
        # Récupère le prix minimum
        min_price = min_price_menu["min_prix"]

        # Vérifie s'il y a au moins un menu de type "plat principal"
        has_main_dish = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).exists()
        
        # Vérifie s'il y a au moins un menu de n'importe quel type
        has_any_menu = Menu.objects.filter(
            restaurant=restaurant
        ).exists()

        # Ajoute le restaurant et son prix minimum à la liste, ainsi que l'indicateur de plat principal
        restaurants_with_min_price.append(
            {
                "restaurant": restaurant, 
                "min_price": min_price, 
                "has_main_dish": has_main_dish,
                "has_any_menu": has_any_menu
            }
        )

    context = {
        'username': username,
        'user_id' : user_id,
        'gerant' : gerant,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        "hotels_with_min_price": hotels_with_min_price,
        "restaurants_with_min_price": restaurants_with_min_price
    }    
    return render(request, 'frontend/Users/user-accueil.html', context)


#Users base
def user_base(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
        context = {
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    } 
        
    return render(request, "frontend/Users/user-base.html", context)


#profile clients
#les reservations du client
def user_mesReservations(request):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    
    reservation_chambre_st = ReservationChambre.objects.filter(user=request.user)
    
    reservation_chambre = sorted(reservation_chambre_st, key=lambda x: x.date_reservation, reverse=True)
    
    reservation_restaurant_st = ReservationRestaurant.objects.filter(user=request.user)
    
    reservation_restaurant = sorted(reservation_restaurant_st, key=lambda x: x.date_reservation, reverse=True)
    
    
    context = {
    "gerant" : gerant,
    'reservation_chambre': reservation_chambre,
    'reservation_restaurant': reservation_restaurant,
    'username': username,
    'user_avatar_url' : user_avatar_url,
    'user_email'  :  user_email,
    } 
    
    return render(request, "frontend/Users/user-mesReservations.html", context)

#liste Hotel client
def user_listeHotel(request):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    hotels = Hotel.objects.all()
    photosHotel = Photo.objects.filter(hotel__in=hotels)
    hotels_with_min_price = []

    for hotel in hotels:
        min_price_chambre = Chambre.objects.filter(hotel=hotel).aggregate(
            Min("tarif_par_nuit")
        )
        min_price = min_price_chambre["tarif_par_nuit__min"]
        hotels_with_min_price.append({"hotel": hotel, "min_price": min_price})

    context = {
        "gerant" : gerant,
        "hotels" : hotels,
        "hotels_with_min_price": hotels_with_min_price,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        'photosHotel' :  photosHotel
        }

    return render(request, "frontend/Users/user-listeHotel.html", context)


#detail Hotel client
def user_detailHotel(request, hotel_id):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)
    photos = Photo.objects.filter(hotel=hotel)
    chambre_avec_prix_minimal = (
        Chambre.objects.filter(hotel=hotel).order_by("tarif_par_nuit").first()
    )
    

    chambres = Chambre.objects.filter(hotel=hotel)[:2]
    photosChambre = PhotoChambre.objects.filter(chambre__in=chambres)

  
    context = {
    "gerant" : gerant,
    "hotel": hotel,
    "prestations": prestations,
    "photos": photos,
    "chambre_avec_prix_minimal": chambre_avec_prix_minimal,
    'username': username,
    'user_avatar_url' : user_avatar_url,
    'user_email'  :  user_email,
    "chambres": chambres,
    "photosChambre": photosChambre
    }

    return render(request, "frontend/Users/user-detailHotel.html", context)



#detail Restaurant client
def user_detailRestaurant(request, restaurant_id):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)
    photos = PhotoRestaurant.objects.filter(restaurant=restaurant)
    menu_avec_prix_minimal = (
        Menu.objects.filter(restaurant=restaurant).order_by("prix").first()
    )
    

    menus = Menu.objects.filter(restaurant=restaurant)[:2]
    photosMenu = PhotoMenu.objects.filter(menu__in=menus)

  
    context = {
    "gerant" : gerant,
    "restaurant": restaurant,
    "prestations": prestations,
    "photos": photos,
    "menu_avec_prix_minimal": menu_avec_prix_minimal,
    'username': username,
    'user_avatar_url' : user_avatar_url,
    'user_email'  :  user_email,
    "menus": menus,
    "photosMenu": photosMenu
    }

    return render(request, "frontend/Users/user-detailRestaurant.html", context)



#liste Restaurant client
def user_listeRestaurant(request):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    gerant = Gerant.objects.filter(user_id=user_id).first()
    restaurants = Restaurant.objects.all()
    photosRestaurant = PhotoRestaurant.objects.filter(restaurant__in=restaurants)
    
    restaurants_with_min_price = []

    for restaurant in restaurants:
        # Filtre les menus par type "plat principal" et calcule le prix minimum
        min_price_menu = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).aggregate(min_prix=Min("prix"))
        
        # Récupère le prix minimum
        min_price = min_price_menu["min_prix"]

        # Vérifie s'il y a au moins un menu de type "plat principal"
        has_main_dish = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).exists()
        
        # Vérifie s'il y a au moins un menu de n'importe quel type
        has_any_menu = Menu.objects.filter(
            restaurant=restaurant
        ).exists()

        # Ajoute le restaurant et son prix minimum à la liste, ainsi que l'indicateur de plat principal
        restaurants_with_min_price.append(
            {
                "restaurant": restaurant, 
                "min_price": min_price, 
                "has_main_dish": has_main_dish,
                "has_any_menu": has_any_menu
            }
        )

    context = {
        "gerant" : gerant,
        "restaurants" : restaurants,
        "restaurants_with_min_price": restaurants_with_min_price,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        'photosRestaurant'  : photosRestaurant
        }

    return render(request, "frontend/Users/user-listeRestaurant.html", context)



def devenirPrestataire(request):
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
        
    context = {
    'pays': pays,
    'username': username,
    'user_avatar_url' : user_avatar_url,
    'user_email'  :  user_email,
    } 
    
    if request.method == "POST":
        # Récupérer les données du gerant
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        pays = request.POST.get("pays")
        coordonnees_tel = request.POST.get("coordonnees_tel")
        adresse = request.POST.get("adresse")
        
        if Gerant.objects.filter(user_id=user_id).first():
            messages.error(
                request, "Une demande que vous avez faite existe déjà. Veuillez patient le temps que cette demande soit approuvée ou non."
            )
            return redirect("devenirPrestataire")

        # Créer l'objet gerant
        gerant = Gerant.objects.create(
            user=request.user,
            nom=nom,
            prenom= prenom,
            pays=pays,
            coordonnees_tel=coordonnees_tel,
            adresse=adresse,
        )

        # Récupérer et associer les documents
        documents = request.FILES.getlist("documents")
        for document in documents:
            DocumentGerant.objects.create(document=document, gerant=gerant)

        messages.success(
            request, f" Votre demande est en cours de validation. Veuillez patient le temps que cette demande soit approuvée ou non."
        )
        return redirect("devenirPrestataire")
    else:
        return render(request, "frontend/Users/user-devenirPrestataire.html", context)



def generate_confirmation_number():
    prefix = "BS-"
    number = random.randint(100000, 999999)
    confirmation_number = f"{prefix}{number}"
    return confirmation_number


#User reserver chambre
def user_reserverChambre(request, chambre_id):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    chambre = get_object_or_404(Chambre, pk=chambre_id)
    
    if request.method == 'POST':
        date_du_jour_str = request.POST.get('date_du_jour')
        date_arrivee = request.POST.get('date_arrivee')
        nombre_personnes = request.POST.get('nombre_personnes')
        moyen_paiement = request.POST.get('moyen_paiement')
        
        # Convertir les dates en objets datetime
        date_du_jour = datetime.strptime(date_du_jour_str, '%d/%b/%Y')
        date_arrivee = datetime.strptime(date_arrivee, '%d/%b/%Y')
        
        # Calculer la durée du séjour en jours
        duree_reservation = (date_arrivee - date_du_jour).days
        
        # Calculer le prix total
        if duree_reservation == 0:
            prix_total = chambre.tarif_reservation_par_jour * 1
        else:
            prix_total = chambre.tarif_reservation_par_jour * (duree_reservation + 1)

        numero_confirmation = generate_confirmation_number()
        
        reservation = ReservationChambre(
            user=request.user,
            chambre=chambre,
            date_arrivee=date_arrivee,
            nombre_personnes=nombre_personnes,
            moyen_paiement=moyen_paiement,
            prix_total=prix_total,
            numero_confirmation=numero_confirmation
        )
        reservation.save()
        messages.success(request, 'Veuillez à présent confirmer votre réservation.')
        return render(request, "frontend/Users/user-confirmerReservationChambre.html", {'reservation': reservation})
    
    context = {
        "gerant" : gerant,
        'chambre': chambre,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }
    
    return render(request, "frontend/Users/user-reserverChambre.html", context)


def user_confirmerReservationChambre(request, reservation_id):
    reservation = get_object_or_404(ReservationChambre, pk=reservation_id)
    reservation.is_confirmer = True
    reservation.save()
    
    
    messages.success(request, "Votre réservation a été effectuée avec succès. Veuillez patient le temps que votre réservation soit approuvée ou non")
    return render(request, "frontend/Users/user-confirmerReservationChambre.html", {'reservation': reservation})



def user_annulerReservationChambre(request, reservation_id):
    reservation = get_object_or_404(ReservationChambre, pk=reservation_id)
    reservation.delete()
    messages.success(request, "Votre réservation a été annuler avec succès.")
    return redirect("accueil")



#User reserver restaurant
def user_reserverRestaurant(request, restaurant_id):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    
    gerant = Gerant.objects.filter(user_id=user_id).first()
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    
    if request.method == 'POST':
        date_arrivee_str = request.POST.get('date_arrivee')
        heure_arrivee_str = request.POST.get('heure_arrivee')
        nombre_personnes = request.POST.get('nombre_personnes')
        moyen_paiement = request.POST.get('moyen_paiement')
        
        
        date_arrivee = datetime.strptime(date_arrivee_str, '%d/%b/%Y').date()
        heure_arrivee = datetime.strptime(heure_arrivee_str, '%H:%M').time()

        numero_confirmation = generate_confirmation_number()
        
        reservation = ReservationRestaurant(
            user=request.user,
            restaurant=restaurant,
            date_arrivee=date_arrivee,
            heure_arrivee=heure_arrivee,
            nombre_personnes=nombre_personnes,
            moyen_paiement=moyen_paiement,
            numero_confirmation=numero_confirmation
        )
        reservation.save()
        messages.success(request, 'Veuillez à présent confirmer votre réservation.')
        return render(request, "frontend/Users/user-confirmerReservationRestaurant.html", {'reservation': reservation})
    
    context = {
        "gerant" : gerant,
        'restaurant': restaurant,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }
    
    return render(request, "frontend/Users/user-reserverRestaurant.html", context)



def user_confirmerReservationRestaurant(request, reservation_id):
    reservation = get_object_or_404(ReservationRestaurant, pk=reservation_id)
    reservation.is_confirmer = True
    reservation.save()
    messages.success(request, "Votre réservation a été effectuée avec succès. Veuillez patient le temps que votre réservation soit approuvée ou non")
    return render(request, "frontend/Users/user-confirmerReservationRestaurant.html", {'reservation': reservation})



def user_annulerReservationRestaurant(request, reservation_id):
    reservation = get_object_or_404(ReservationRestaurant, pk=reservation_id)
    reservation.delete()
    messages.success(request, "Votre réservation a été annuler avec succès.")
    return redirect("accueil")


def user_dash_admin(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    user_hotels_count = 0
    user_chambres_count = 0
    user_restaurants_count = 0
    user_menus_count = 0
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    user_hotels = Hotel.objects.filter(proprietaire=request.user)
    user_hotels_count = user_hotels.count()
    user_chambres = Chambre.objects.filter(proprietaire=request.user)
    user_chambres_count = user_chambres.count()
    user_restaurants = Restaurant.objects.filter(proprietaire=request.user)
    user_restaurants_count = user_restaurants.count()
    user_menus = Menu.objects.filter(proprietaire=request.user)
    user_menus_count = user_menus.count()
    
        
    
    context = {
    'user_hotels_count': user_hotels_count,
    'user_chambres_count': user_chambres_count,
    'user_restaurants_count': user_restaurants_count,
    'user_menus_count': user_menus_count,
    'username': username,
    'user_avatar_url' : user_avatar_url,
    'user_email'  :  user_email,
    }
    return render(request, "frontend/Users/user-dash-admin.html", context)


# Authetification
def login(request):
    return render(request, "frontend/connexion.html")


def sign_up(request):
    return render(request, "frontend/inscription.html")

def user_paiement_restaurant(request, reservation_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
     
    reservation = get_object_or_404(ReservationRestaurant, pk=reservation_id)
        
    if request.method == "POST":
        votre_numero_telephone = request.POST.get("votre_numero_telephone") 
        numero_telephone_destinataire = request.POST.get("numero_telephone_destinataire") 
        montant = float(
            request.POST.get("montant").replace(",", ".").replace("\xa0", "")
        )
        
        reservation.statut_paiement = True
        reservation.save()
        
        ReservationRestaurantPaiement.objects.create(
                reservation = reservation,
                votre_numero_telephone=votre_numero_telephone,
                numero_telephone_destinataire=numero_telephone_destinataire,
                montant=montant,
            )
 
        messages.success(request, f"Le payement a été éffectué avec succès. Votre réservation est à présent complet et valide")
        
        return redirect("user-mesReservations")    
    
    
    
    context = {
        "reservation": reservation,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }
    return render(request, "frontend/Users/user-paiement-restaurant.html", context)


def user_paiement_hotel(request, reservation_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
     
    reservation = get_object_or_404(ReservationChambre, pk=reservation_id)
        
    if request.method == "POST":
        votre_numero_telephone = request.POST.get("votre_numero_telephone") 
        numero_telephone_destinataire = request.POST.get("numero_telephone_destinataire") 
        montant = float(
            request.POST.get("montant").replace(",", ".").replace("\xa0", "")
        )
        
        reservation.statut_paiement = True
        reservation.save()
        
        ReservationHotelPaiement.objects.create(
                reservation = reservation,
                votre_numero_telephone=votre_numero_telephone,
                numero_telephone_destinataire=numero_telephone_destinataire,
                montant=montant,
            )
 
        messages.success(request, f"Le payement a été éffectué avec succès. Votre réservation est à présent complet et valide")
        
        return redirect("user-mesReservations")    
    
    
    
    context = {
        "reservation": reservation,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }
    return render(request, "frontend/Users/user-paiement-hotel.html", context)



def user_admin_listeReservationHotels(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    # Récupérer toutes les chambres appartenant au propriétaire
    chambres = Chambre.objects.filter(proprietaire=request.user)
    
    # Récupérer toutes les réservations pour ces chambres
    reservations = ReservationChambre.objects.filter(chambre__in=chambres)
    
    context = {
        "reservations": reservations,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }
        
    return render(request, "frontend/Users/user-admin-listeReservationHotels.html", context)


#Validation accepter hotel
def validation_accepter_reservation_hotel(request, reservation_id):
    reservation = get_object_or_404(ReservationChambre, pk=reservation_id)
    reservation.validation = "Validée"
    reservation.save()
    
    messages.success(request, f"La reservation '{reservation.numero_confirmation}' a été accepté.")
    return redirect('user-admin-listeReservationHotels')

#validation refuser hotel
def validation_refuser_reservation_hotel(request, reservation_id):
    reservation = get_object_or_404(ReservationChambre, pk=reservation_id)
    reservation.validation = "Refusée"
    reservation.save()
    
    messages.success(request, f"La reservation '{reservation.numero_confirmation}' a été refusé.")
    return redirect('user-admin-listeReservationHotels')



def user_admin_listeReservationRestaurants(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    # Récupérer toutes les chambres appartenant au propriétaire
    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    
    # Récupérer toutes les réservations pour ces chambres
    reservations = ReservationRestaurant.objects.filter(restaurant__in=restaurants)
    
    context = {
        "reservations": reservations,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }
        
    return render(request, "frontend/Users/user-admin-listeReservationRestaurants.html", context)


#Validation accepter restaurant
def validation_accepter_reservation_restaurant(request, reservation_id):
    reservation = get_object_or_404(ReservationRestaurant, pk=reservation_id)
    reservation.validation = "Validée"
    reservation.save()
    
    messages.success(request, f"La reservation '{reservation.numero_confirmation}' a été accepté.")
    return redirect('user-admin-listeReservationRestaurants')

#validation refuser restaurant
def validation_refuser_reservation_restaurant(request, reservation_id):
    reservation = get_object_or_404(ReservationRestaurant, pk=reservation_id)
    reservation.validation = "Refusée"
    reservation.save()
    
    messages.success(request, f"La reservation '{reservation.numero_confirmation}' a été refusé.")
    return redirect('user-admin-listeReservationRestaurants')



#ajouter chambre gerant
def user_admin_ajouterChambre(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    hotels = Hotel.objects.filter(proprietaire=request.user)
    context = {
        "hotels": hotels,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        hotel_id = request.POST.get("hotel")
        type_de_chambre = request.POST.get("type_de_chambre")
        surface = request.POST.get("surface")
        tarif_par_nuit = request.POST.get("tarif_par_nuit")
        tarif_reservation_par_jour = request.POST.get("tarif_reservation_par_jour")
        vue_sur_mer = request.POST.get(
            "vue_sur_mer"
        )  # Récupérer la valeur sélectionnée
        emplacement = request.POST.get("emplacement")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        hotel = Hotel.objects.get(id=hotel_id)

        chambre = Chambre.objects.create(
            proprietaire=request.user,
            nom=nom,
            description=description,
            hotel=hotel,
            type_de_chambre=type_de_chambre,
            surface=surface,
            tarif_par_nuit=tarif_par_nuit,
            tarif_reservation_par_jour = tarif_reservation_par_jour,
            vue_sur_mer=vue_sur_mer,  # Enregistrer la valeur sélectionnée
            emplacement=emplacement,
            photo=first_photo,
        )

        photos = request.FILES.getlist("images")
        for photo in photos:
            PhotoChambre.objects.create(image=photo, chambre=chambre)

        return redirect("user-admin-listeChambre")

    return render(request, "frontend/Users/user-admin-ajouterChambre.html", context)



#liste chambre gerant
@login_required
def user_admin_listeChambre(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    

    chambres = Chambre.objects.filter(proprietaire=request.user)
    context = {
        "chambres": chambres,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/Users/user-admin-listeChambre.html", context)



#detail chambre gerant
def user_admin_detailChambre(request, chambre_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    
    chambre = get_object_or_404(Chambre, pk=chambre_id)
    photos = PhotoChambre.objects.filter(chambre=chambre)
    context = {
            "chambre": chambre,
            "photos": photos,
            'username': username,
            'user_avatar_url' : user_avatar_url,
            'user_email'  :  user_email,

            }

    return render(request, "frontend/Users/user-admin-detailChambre.html", context)



#modifier chambre gerant
def user_admin_modifierChambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, pk=chambre_id)

    if request.method == "POST":
        chambre.nom = request.POST.get("nom")
        chambre.description = request.POST.get("description")
        chambre.type_de_chambre = request.POST.get("type_de_chambre")
        chambre.surface = float(
            request.POST.get("surface").replace(",", ".").replace("\xa0", "")
        )
        chambre.tarif_par_nuit = float(
            request.POST.get("tarif_par_nuit").replace(",", ".").replace("\xa0", "")
        )
        chambre.tarif_reservation_par_jour = float(
            request.POST.get("tarif_reservation_par_jour").replace(",", ".").replace("\xa0", "")
        )
        chambre.vue_sur_mer = request.POST.get("vue_sur_mer")
        chambre.emplacement = request.POST.get("emplacement")
        chambre.hotel_id = request.POST.get("hotel")

        if request.FILES.get("photo"):
            chambre.photo = request.FILES.get("photo")

        chambre.save()
        messages.success(
            request, f"La chambre '{chambre.nom}' a été mise à jour avec succès."
        )
        return redirect("user-admin-listeChambre")


    hotels = Hotel.objects.filter(proprietaire=request.user)
    context = {"hotels": hotels, "chambre": chambre}

    return render(request, "frontend/Users/user-admin-modifierChambre.html", context)



#supprimer chambre gerant
def user_admin_supprimerChambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, pk=chambre_id)
    photos = PhotoChambre.objects.filter(chambre=chambre)

    photos.delete()
    chambre.delete()

    messages.success(request, f"La chambre '{chambre.nom}'a été supprimée avec succès.")

    return redirect("user-admin-listeChambre")


#ajouter Hotel gerant
@login_required
def user_admin_ajouterHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
        
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    context = {
        "pays": pays,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,}

    if request.method == "POST":
        # Récupérer les données de l'hôtel
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        adresse = request.POST.get("adresse")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        coordonnees_tel = request.POST.get("coordonnees_tel")
        nombre_de_chambres = request.POST.get("nombre_de_chambres")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        # Créer l'objet Hotel
        hotel = Hotel.objects.create(
            proprietaire=request.user,
            nom=nom,
            description=description,
            statut=statut,
            adresse=adresse,
            ville=ville,
            pays=pays,
            coordonnees_tel=coordonnees_tel,
            nombre_de_chambres=nombre_de_chambres,
            photo=first_photo,
        )

        # Récupérer et associer les photos
        photos = request.FILES.getlist("images")
        for photo in photos:
            Photo.objects.create(image=photo, hotel=hotel)

        return redirect("user-admin-listeHotel")
    else:
        return render(request, "frontend/Users/user-admin-ajouterHotel.html", context)

#liste Hotel gerant
@login_required
def user_admin_listeHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
       
    hotels = Hotel.objects.filter(proprietaire=request.user)
    hotels_with_min_price = []

    for hotel in hotels:
        min_price_chambre = Chambre.objects.filter(hotel=hotel).aggregate(
            Min("tarif_par_nuit")
        )
        min_price = min_price_chambre["tarif_par_nuit__min"]
        hotels_with_min_price.append({"hotel": hotel, "min_price": min_price})

    context = {
        "hotels" : hotels,
        "hotels_with_min_price": hotels_with_min_price,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }
    return render(request, "frontend/Users/user-admin-listeHotel.html", context)

#modifier Hotel gerant
def user_admin_modifierHotel(request, hotel_id):
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    hotel = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == "POST":
        hotel.nom = request.POST.get("nom")
        hotel.description = request.POST.get("description")
        hotel.statut = request.POST.get("statut")
        hotel.adresse = request.POST.get("adresse")
        hotel.ville = request.POST.get("ville")
        hotel.pays = request.POST.get("pays")
        hotel.coordonnees_tel = request.POST.get("coordonnees_tel")
        hotel.nombre_de_chambres = request.POST.get("nombre_de_chambres")

        if request.FILES.get("photo"):
            hotel.photo = request.FILES.get("photo")

        hotel.save()
        messages.success(
            request, f"L'hôtel '{hotel.nom}' a été mise à jour avec succès."
        )
        return redirect("user-admin-listeHotel")

    hotels = Hotel.objects.filter(proprietaire=request.user)
    context = {"hotels": hotels, "hotel": hotel, "pays": pays}

    return render(request, "frontend/Users/user-admin-modifierHotel.html", context)

#supprimer Hotel gerant
def user_admin_supprimerHotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    photos_hotel = Photo.objects.filter(hotel=hotel)
    chambres = Chambre.objects.filter(hotel=hotel)

    for chambre in chambres:
        photos_chambre = PhotoChambre.objects.filter(chambre=chambre)
        photos_chambre.delete()

    photos_hotel.delete()
    chambres.delete()
    hotel.delete()

    messages.success(request, f"L'hôtel {hotel.nom} a été supprimée avec succès.")

    return redirect("user-admin-listeHotel")


#detail Hotel gerant
def user_admin_detailHotel(request, hotel_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)
    photos = Photo.objects.filter(hotel=hotel)
    chambre_avec_prix_minimal = (
        Chambre.objects.filter(hotel=hotel).order_by("tarif_par_nuit").first()
    )
    context = {
        "hotel": hotel,
        "prestations": prestations,
        "photos": photos,
        "chambre_avec_prix_minimal": chambre_avec_prix_minimal,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }

    return render(request, "frontend/Users/user-admin-detailHotel.html", context)


#ajouter Prestations gerant
def user_admin_ajouterPrestationHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    if request.method == "POST":
        hotel_id = request.POST.get("hotel")
        
        # Vérifiez si une prestation existe déjà pour cet hôtel
        if PrestationHotel.objects.filter(hotel_id=hotel_id).exists():
            messages.error(
                request, "Une prestation existe déjà pour cet hôtel. Vous ne pouvez pas créer plusieurs prestations pour le même hôtel."
            )
            return redirect("user-admin-ajouterPrestationHotel")
        
        activites = {
            "piscine": request.POST.get("piscine", "non") == "oui",
            "spa": request.POST.get("spa", "non") == "oui",
            "salle_de_sport": request.POST.get("salle_de_sport", "non") == "oui",
            "aire_de_jeux": request.POST.get("aire_de_jeux", "non") == "oui",
        }
        services = {
            "nettoyage_a_sec": request.POST.get("nettoyage_a_sec", "non") == "oui",
            "service_de_chambre": request.POST.get("service_de_chambre", "non")
            == "oui",
            "service_special": request.POST.get("service_special", "non") == "oui",
            "aire_dattente": request.POST.get("aire_dattente", "non") == "oui",
            "concierge": request.POST.get("concierge", "non") == "oui",
            "service_de_repassage": request.POST.get("service_de_repassage", "non")
            == "oui",
            "wifi_gratuit": request.POST.get("wifi_gratuit", "non") == "oui",
            "ascenseur": request.POST.get("ascenseur", "non") == "oui",
        }
        reception_evenements = {
            "reception_evenements": request.POST.get("reception_evenements", "non")
            == "oui",
            "salle_conference": request.POST.get("salle_conference", "non") == "oui",
            "salle_reunion": request.POST.get("salle_reunion", "non") == "oui",
            "equipement_audiovisuel": request.POST.get("equipement_audiovisuel", "non")
            == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        hotel = get_object_or_404(Hotel, pk=hotel_id)
        prestations = PrestationHotel(
            hotel=hotel,
            activites=activites,
            services=services,
            reception_evenements=reception_evenements,
            langues_personnel=langues_personnel,
            methodes_paiement=methodes_paiement,
        )
        prestations.save()

        messages.success(
            request, f"La prestation de l'hôtel '{hotel.nom}' a été ajoutée avec succès."
        )
        return redirect("user-admin-listeHotel")

    hotels = Hotel.objects.filter(proprietaire=request.user)
    context = {
        "hotels": hotels,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/Users/user-admin-ajouterPrestationHotel.html", context)
#supprimer Prestations gerant
def user_admin_supprimerPrestationHotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)

    prestations.delete()

    messages.success(
        request, f" la prestation de l'hôtel {hotel.nom} a été supprimée avec succès."
    )

    return redirect("user-admin-listeHotel")


#modifier Prestations gerant
def user_admin_modifierPrestationHotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)

    if request.method == "POST":
        hotel_id = request.POST.get("hotel")
        activites = {
            "piscine": request.POST.get("piscine", "non") == "oui",
            "spa": request.POST.get("spa", "non") == "oui",
            "salle_de_sport": request.POST.get("salle_de_sport", "non") == "oui",
            "aire_de_jeux": request.POST.get("aire_de_jeux", "non") == "oui",
        }
        services = {
            "nettoyage_a_sec": request.POST.get("nettoyage_a_sec", "non") == "oui",
            "service_de_chambre": request.POST.get("service_de_chambre", "non")
            == "oui",
            "service_special": request.POST.get("service_special", "non") == "oui",
            "aire_dattente": request.POST.get("aire_dattente", "non") == "oui",
            "concierge": request.POST.get("concierge", "non") == "oui",
            "service_de_repassage": request.POST.get("service_de_repassage", "non")
            == "oui",
            "wifi_gratuit": request.POST.get("wifi_gratuit", "non") == "oui",
            "ascenseur": request.POST.get("ascenseur", "non") == "oui",
        }
        reception_evenements = {
            "reception_evenements": request.POST.get("reception_evenements", "non")
            == "oui",
            "salle_conference": request.POST.get("salle_conference", "non") == "oui",
            "salle_reunion": request.POST.get("salle_reunion", "non") == "oui",
            "equipement_audiovisuel": request.POST.get("equipement_audiovisuel", "non")
            == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        for prestation in prestations:
            prestation.activites = activites
            prestation.services = services
            prestation.reception_evenements = reception_evenements
            prestation.langues_personnel = langues_personnel
            prestation.methodes_paiement = methodes_paiement
            prestation.save()

        messages.success(
            request, f" la prestation de l'hôtel {hotel.nom} a été modifié avec succès."
        )

        return redirect("user-admin-listeHotel")

    hotels = Hotel.objects.filter(proprietaire=request.user)
    context = {"hotels": hotels, "prestations": prestations}

    return render(request, "frontend/Users/user-admin-modifierPrestationHotel.html", context)


#Restaurant

#ajouter restaurant gerant
def user_admin_ajouterRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    context = {
        "pays": pays,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        # Récupérer les données du restaurant
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        adresse = request.POST.get("adresse")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        coordonnees_tel = request.POST.get("coordonnees_tel")
        nombre_de_tables = request.POST.get("nombre_de_tables")
        prix_reservation = request.POST.get("prix_reservation")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        # Créer l'objet restaurant
        restaurant = Restaurant.objects.create(
            proprietaire=request.user,
            nom=nom,
            description=description,
            statut=statut,
            adresse=adresse,
            ville=ville,
            pays=pays,
            coordonnees_tel=coordonnees_tel,
            nombre_de_tables=nombre_de_tables,
            prix_reservation=prix_reservation,
            photo=first_photo,
        )

        # Récupérer et associer les photos
        photos = request.FILES.getlist("images")
        for photo in photos:
            PhotoRestaurant.objects.create(image=photo, restaurant=restaurant)

        return redirect("user-admin-listeRestaurant")
    else:
        return render(request, "frontend/Users/user-admin-ajouterRestaurant.html", context)



#liste restaurant gerant
@login_required
def user_admin_listeRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    
    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    restaurants_with_min_price = []

    for restaurant in restaurants:
        # Filtre les menus par type "plat principal" et calcule le prix minimum
        min_price_menu = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).aggregate(min_prix=Min("prix"))
        
        # Récupère le prix minimum
        min_price = min_price_menu["min_prix"]

        # Vérifie s'il y a au moins un menu de type "plat principal"
        has_main_dish = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).exists()
        
        # Vérifie s'il y a au moins un menu de n'importe quel type
        has_any_menu = Menu.objects.filter(
            restaurant=restaurant
        ).exists()

        # Ajoute le restaurant et son prix minimum à la liste, ainsi que l'indicateur de plat principal
        restaurants_with_min_price.append(
            {
                "restaurant": restaurant, 
                "min_price": min_price, 
                "has_main_dish": has_main_dish,
                "has_any_menu": has_any_menu
            }
        )

    context = {
        "restaurants" : restaurants,
        "restaurants_with_min_price": restaurants_with_min_price,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }
    
    return render(request, "frontend/Users/user-admin-listeRestaurant.html", context)


#detail Restaurant gerant
def user_admin_detailRestaurant(request, restaurant_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)
    photos = PhotoRestaurant.objects.filter(restaurant=restaurant)
    menu_avec_prix_minimal = (
        Menu.objects.filter(restaurant=restaurant).order_by("prix").first()
    )
    context = {
        "restaurant": restaurant,
        "prestations": prestations,
        "photos": photos,
        "menu_avec_prix_minimal": menu_avec_prix_minimal,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }

    return render(request, "frontend/Users/user-admin-detailRestaurant.html", context)


#modifier restaurant gerant
def user_admin_modifierRestaurant(request, restaurant_id):
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    if request.method == "POST":
        restaurant.nom = request.POST.get("nom")
        restaurant.description = request.POST.get("description")
        restaurant.statut = request.POST.get("statut")
        restaurant.adresse = request.POST.get("adresse")
        restaurant.ville = request.POST.get("ville")
        restaurant.pays = request.POST.get("pays")
        restaurant.coordonnees_tel = request.POST.get("coordonnees_tel")
        restaurant.nombre_de_tables = request.POST.get("nombre_de_tables")
        restaurant.prix_reservation = request.POST.get("prix_reservation")

        if request.FILES.get("photo"):
            restaurant.photo = request.FILES.get("photo")

        restaurant.save()
        messages.success(
            request, f"Le restaurant '{restaurant.nom}' a été mise à jour avec succès."
        )
        return redirect("user-admin-listeRestaurant")

    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    context = {"restaurants": restaurants, "restaurant": restaurant, "pays": pays}

    return render(request, "frontend/Users/user-admin-modifierRestaurant.html", context)



#supprimer restaurant gerant
def user_admin_supprimerRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    photos_restaurant = Photo.objects.filter(restaurant=restaurant)
    menus = Menu.objects.filter(menu=menu)

    for menu in menus:
        photos_menu = PhotoMenu.objects.filter(menu=menu)
        photos_menu.delete()

    photos_restaurant.delete()
    menu.delete()
    restaurant.delete()

    messages.success(
        request, f"Le restaurant {restaurant.nom} a été supprimée avec succès."
    )

    return redirect("user-admin-listeRestaurant")



#Menu

#ajouter un menu gerant
def user_admin_ajouterMenu(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    context = {
        "restaurants": restaurants,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        restaurant_id = request.POST.get("restaurant")
        type_de_plat = request.POST.get("type_de_plat")
        prix = request.POST.get("prix")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        restaurant = Restaurant.objects.get(id=restaurant_id)

        menu = Menu.objects.create(
            proprietaire=request.user,
            nom=nom,
            description=description,
            restaurant=restaurant,
            type_de_plat=type_de_plat,
            prix=prix,
            photo=first_photo,
        )

        photos = request.FILES.getlist("images")
        for photo in photos:
            PhotoMenu.objects.create(image=photo, menu=menu)

        return redirect("user-admin-listeMenu")

    return render(request, "frontend//Users/user-admin-ajouterMenu.html", context)


#liste menu gerant
@login_required
def user_admin_listeMenu(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        

    menus = Menu.objects.filter(proprietaire=request.user)
    context = {
        "menus": menus,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
}

    return render(request, "frontend/Users/user-admin-listeMenu.html", context)


#Modifier menu gerant
def user_admin_modifierMenu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)

    if request.method == "POST":
        
        menu.nom = request.POST.get("nom")
        menu.description = request.POST.get("description")
        menu.restaurant_id = request.POST.get("restaurant")
        menu.type_de_plat = request.POST.get("type_de_plat")
        menu.prix = float(
            request.POST.get("prix").replace(",", ".").replace("\xa0", "")
        )

        menu.restaurant_id = request.POST.get("restaurant")

        if request.FILES.get("photo"):
            menu.photo = request.FILES.get("photo")

        menu.save()
        messages.success(request, f"Le menu'{menu.nom}' a été mise à jour avec succès.")
        return redirect("user-admin-listeMenu")

    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    context = {"restaurants": restaurants, "menu": menu}

    return render(request, "frontend/Users/user-admin-modifierMenu.html", context)



#supprimer menu gerant
def user_admin_supprimerMenu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    photos = PhotoMenu.objects.filter(menu=menu)

    photos.delete()
    menu.delete()

    messages.success(request, f"Le menu '{menu.nom}'a été supprimée avec succès.")

    return redirect("user-admin-listeMenu")



#ajouter Prestation de restaurant gerant
def user_admin_ajouterPrestationRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    
    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant")
        services = {
            "diners_avec_spectacle": request.POST.get("diners_avec_spectacle", "non") == "oui",
            "soirees_a_theme": request.POST.get("soirees_a_theme", "non") == "oui",
            "menus_degustation": request.POST.get("menus_degustation", "non") == "oui",
            "diners_prives": request.POST.get("diners_prives", "non") == "oui",
            "programmes_de_fidelite": request.POST.get("programmes_de_fidelite", "non") == "oui",
            "anniversaire": request.POST.get("anniversaire", "non") == "oui",
        }

        types_de_cuisine  = {
            "mexicaine": request.POST.get("mexicaine", "non") == "oui",
            "chinoise": request.POST.get("chinoise", "non") == "oui",
            "japonaise": request.POST.get("japonaise", "non") == "oui",
            "française": request.POST.get("française", "non") == "oui",
            "africaine": request.POST.get("africaine", "non") == "oui",
            "autres": request.POST.get("autres", "non") == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        
        if PrestationRestaurant.objects.filter(restaurant_id=restaurant_id).exists():
            messages.error(
                request, "Une prestation existe déjà pour ce restaurant. Vous ne pouvez pas créer plusieurs prestations pour le même restaurant."
            )
            return redirect("user-admin-ajouterPrestationRestaurant")
        
        prestations = PrestationRestaurant(
            restaurant=restaurant,
            services=services,
            types_de_cuisine=types_de_cuisine,
            langues_personnel=langues_personnel,
            methodes_paiement=methodes_paiement,
        )
        prestations.save()

        messages.success(
            request, f"La prestation du restaurant '{restaurant.nom}' a été ajouter avec succès."
        )
        return redirect("user-admin-listeRestaurant")

    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    context = {
        "restaurants": restaurants,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/Users/user-admin-ajouterPrestationRestaurant.html", context)



def user_admin_supprimerPrestationRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)

    prestations.delete()

    messages.success(
        request,
        f" la prestation du restaurant '{restaurant.nom}' a été supprimée avec succès.",
    )

    return redirect("user-admin-listeRestaurant")


def user_admin_modifierPrestationRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)

    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant")
        services = {
            "diners_avec_spectacle": request.POST.get("diners_avec_spectacle", "non") == "oui",
            "soirees_a_theme": request.POST.get("soirees_a_theme", "non") == "oui",
            "menus_degustation": request.POST.get("menus_degustation", "non") == "oui",
            "diners_prives": request.POST.get("diners_prives", "non") == "oui",
            "programmes_de_fidelite": request.POST.get("programmes_de_fidelite", "non") == "oui",
            "anniversaire": request.POST.get("anniversaire", "non") == "oui",
        }

        types_de_cuisine  = {
            "mexicaine": request.POST.get("mexicaine", "non") == "oui",
            "chinoise": request.POST.get("chinoise", "non") == "oui",
            "japonaise": request.POST.get("japonaise", "non") == "oui",
            "française": request.POST.get("française", "non") == "oui",
            "africaine": request.POST.get("africaine", "non") == "oui",
            "autres": request.POST.get("autres", "non") == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        for prestation in prestations:
            prestation.services = services
            prestation.types_de_cuisine  = types_de_cuisine
            prestation.langues_personnel = langues_personnel
            prestation.methodes_paiement = methodes_paiement
            prestation.save()

        messages.success(
            request,
            f" la prestation du restaurant '{restaurant.nom}' a été modifié avec succès.",
        )

        return redirect("user-admin-listeRestaurant")

    restaurants = Restaurant.objects.filter(proprietaire=request.user)
    context = {"restaurants": restaurants, "prestations": prestations}

    return render(request, "frontend/Users/user-admin-modifierPrestationRestaurant.html", context)





# Dashbord
def dashboard(request):
    # context = {"message" : "Hello world !"}
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Récupère le nom d'utilisateur
    user_avatar_url = None
    user_hotels_count = 0
    user_chambres_count = 0
    user_restaurants_count = 0
    user_menus_count = 0
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    user_hotels = Hotel.objects.all()
    user_hotels_count = user_hotels.count()
    user_chambres = Chambre.objects.all()
    user_chambres_count = user_chambres.count()
    user_restaurants = Restaurant.objects.all()
    user_restaurants_count = user_restaurants.count()
    user_menus = Menu.objects.all()
    user_menus_count = user_menus.count()
    
        
    
    context = {
    'user_hotels_count': user_hotels_count,
    'user_chambres_count': user_chambres_count,
    'user_restaurants_count': user_restaurants_count,
    'user_menus_count': user_menus_count,
        'username': username,
        'user_avatar_url': user_avatar_url,
        'user_email': user_email,
    }
    
    return render(request, "frontend/admin-dashboard.html", context)


# Fichier de base
def base(request):
    return render(request, "frontend/base.html")


# Hotellerie


def ajouterHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
        
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    context = {
        "pays": pays,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        # Récupérer les données de l'hôtel
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        adresse = request.POST.get("adresse")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        coordonnees_tel = request.POST.get("coordonnees_tel")
        nombre_de_chambres = request.POST.get("nombre_de_chambres")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        # Créer l'objet Hotel
        hotel = Hotel.objects.create(
            nom=nom,
            description=description,
            statut=statut,
            adresse=adresse,
            ville=ville,
            pays=pays,
            coordonnees_tel=coordonnees_tel,
            nombre_de_chambres=nombre_de_chambres,
            photo=first_photo,
        )

        # Récupérer et associer les photos
        photos = request.FILES.getlist("images")
        for photo in photos:
            Photo.objects.create(image=photo, hotel=hotel)

        return redirect("listeHotel")
    else:
        return render(request, "frontend/admin-ajouterHotel.html", context)


def listeHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    hotels = Hotel.objects.all()
    hotels_with_min_price = []

    for hotel in hotels:
        min_price_chambre = Chambre.objects.filter(hotel=hotel).aggregate(
            Min("tarif_par_nuit")
        )
        min_price = min_price_chambre["tarif_par_nuit__min"]
        hotels_with_min_price.append({"hotel": hotel, "min_price": min_price})

    context = {
        "hotels_with_min_price": hotels_with_min_price,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }
    return render(request, "frontend/admin-listeHotel.html", context)


def modifierHotel(request, hotel_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
 
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    hotel = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == "POST":
        hotel.nom = request.POST.get("nom")
        hotel.description = request.POST.get("description")
        hotel.statut = request.POST.get("statut")
        hotel.adresse = request.POST.get("adresse")
        hotel.ville = request.POST.get("ville")
        hotel.pays = request.POST.get("pays")
        hotel.coordonnees_tel = request.POST.get("coordonnees_tel")
        hotel.nombre_de_chambres = request.POST.get("nombre_de_chambres")

        if request.FILES.get("photo"):
            hotel.photo = request.FILES.get("photo")

        hotel.save()
        messages.success(
            request, f"L'hôtel '{hotel.nom}' a été mise à jour avec succès."
        )
        return redirect("listeHotel")

    hotels = Hotel.objects.all()
    context = {
            "hotels": hotels,
            "hotel": hotel,
            "pays": pays,
            'username': username,
            'user_avatar_url' : user_avatar_url,
            'user_email'  :  user_email,}

    return render(request, "frontend/admin-modifierHotel.html", context)


def supprimerHotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    photos_hotel = Photo.objects.filter(hotel=hotel)
    chambres = Chambre.objects.filter(hotel=hotel)

    for chambre in chambres:
        photos_chambre = PhotoChambre.objects.filter(chambre=chambre)
        photos_chambre.delete()

    photos_hotel.delete()
    chambres.delete()
    hotel.delete()

    messages.success(request, f"L'hôtel {hotel.nom} a été supprimée avec succès.")

    return redirect("listeHotel")


def detailHotel(request, hotel_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)
    photos = Photo.objects.filter(hotel=hotel)
    chambre_avec_prix_minimal = (
        Chambre.objects.filter(hotel=hotel).order_by("tarif_par_nuit").first()
    )
    context = {
        "hotel": hotel,
        "prestations": prestations,
        "photos": photos,
        "chambre_avec_prix_minimal": chambre_avec_prix_minimal,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }

    return render(request, "frontend/admin-detailHotel.html", context)


def ajouterChambre(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    hotels = Hotel.objects.all()
    context = {
        "hotels": hotels,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        hotel_id = request.POST.get("hotel")
        type_de_chambre = request.POST.get("type_de_chambre")
        surface = request.POST.get("surface")
        tarif_par_nuit = request.POST.get("tarif_par_nuit")
        vue_sur_mer = request.POST.get(
            "vue_sur_mer"
        )  # Récupérer la valeur sélectionnée
        emplacement = request.POST.get("emplacement")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        hotel = Hotel.objects.get(id=hotel_id)

        chambre = Chambre.objects.create(
            nom=nom,
            description=description,
            hotel=hotel,
            type_de_chambre=type_de_chambre,
            surface=surface,
            tarif_par_nuit=tarif_par_nuit,
            vue_sur_mer=vue_sur_mer,  # Enregistrer la valeur sélectionnée
            emplacement=emplacement,
            photo=first_photo,
        )

        photos = request.FILES.getlist("images")
        for photo in photos:
            PhotoChambre.objects.create(image=photo, chambre=chambre)

        return redirect("listeChambre")

    return render(request, "frontend/admin-ajouterChambre.html", context)


def listeChambre(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    chambres = Chambre.objects.all()
    context = {
        "chambres": chambres,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-listeChambre.html", context)


def supprimerChambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, pk=chambre_id)
    photos = PhotoChambre.objects.filter(chambre=chambre)

    photos.delete()
    chambre.delete()

    messages.success(request, f"La chambre '{chambre.nom}'a été supprimée avec succès.")

    return redirect("listeChambre")


def modifierChambre(request, chambre_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    chambre = get_object_or_404(Chambre, pk=chambre_id)

    if request.method == "POST":
        chambre.nom = request.POST.get("nom")
        chambre.description = request.POST.get("description")
        chambre.type_de_chambre = request.POST.get("type_de_chambre")
        chambre.surface = float(
            request.POST.get("surface").replace(",", ".").replace("\xa0", "")
        )
        chambre.tarif_par_nuit = float(
            request.POST.get("tarif_par_nuit").replace(",", ".").replace("\xa0", "")
        )
        chambre.vue_sur_mer = request.POST.get("vue_sur_mer")
        chambre.emplacement = request.POST.get("emplacement")
        chambre.hotel_id = request.POST.get("hotel")

        if request.FILES.get("photo"):
            chambre.photo = request.FILES.get("photo")

        chambre.save()
        messages.success(
            request, f"La chambre '{chambre.nom}' a été mise à jour avec succès."
        )
        return redirect("listeChambre")

    hotels = Hotel.objects.all()
    context = {
            "hotels": hotels,
            "chambre": chambre,
            'username': username,
            'user_avatar_url' : user_avatar_url,
            'user_email'  :  user_email,
            }

    return render(request, "frontend/admin-modifierChambre.html", context)


def detailChambre(request, chambre_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    chambre = get_object_or_404(Chambre, pk=chambre_id)
    photos = PhotoChambre.objects.filter(chambre=chambre)
    context = {
        "chambre": chambre,
        "photos": photos,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-detailChambre.html", context)


def ajouterPrestationHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    if request.method == "POST":
        hotel_id = request.POST.get("hotel")
        activites = {
            "piscine": request.POST.get("piscine", "non") == "oui",
            "spa": request.POST.get("spa", "non") == "oui",
            "salle_de_sport": request.POST.get("salle_de_sport", "non") == "oui",
            "aire_de_jeux": request.POST.get("aire_de_jeux", "non") == "oui",
        }
        services = {
            "nettoyage_a_sec": request.POST.get("nettoyage_a_sec", "non") == "oui",
            "service_de_chambre": request.POST.get("service_de_chambre", "non")
            == "oui",
            "service_special": request.POST.get("service_special", "non") == "oui",
            "aire_dattente": request.POST.get("aire_dattente", "non") == "oui",
            "concierge": request.POST.get("concierge", "non") == "oui",
            "service_de_repassage": request.POST.get("service_de_repassage", "non")
            == "oui",
            "wifi_gratuit": request.POST.get("wifi_gratuit", "non") == "oui",
            "ascenseur": request.POST.get("ascenseur", "non") == "oui",
        }
        reception_evenements = {
            "reception_evenements": request.POST.get("reception_evenements", "non")
            == "oui",
            "salle_conference": request.POST.get("salle_conference", "non") == "oui",
            "salle_reunion": request.POST.get("salle_reunion", "non") == "oui",
            "equipement_audiovisuel": request.POST.get("equipement_audiovisuel", "non")
            == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        hotel = get_object_or_404(Hotel, pk=hotel_id)
        prestations = PrestationHotel(
            hotel=hotel,
            activites=activites,
            services=services,
            reception_evenements=reception_evenements,
            langues_personnel=langues_personnel,
            methodes_paiement=methodes_paiement,
        )
        prestations.save()

        messages.success(
            request, f"La prestation de l'hôtel '{hotel.nom}'a été ajouter avec succès."
        )
        return redirect("listeHotel")

    hotels = Hotel.objects.all()
    context = {
        "hotels": hotels,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-ajouterPrestationHotel.html", context)


def supprimerPrestationHotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)

    prestations.delete()

    messages.success(
        request, f" la prestation de l'hôtel {hotel.nom} a été supprimée avec succès."
    )

    return redirect("listeHotel")


def modifierPrestationHotel(request, hotel_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    prestations = PrestationHotel.objects.filter(hotel=hotel)

    if request.method == "POST":
        hotel_id = request.POST.get("hotel")
        activites = {
            "piscine": request.POST.get("piscine", "non") == "oui",
            "spa": request.POST.get("spa", "non") == "oui",
            "salle_de_sport": request.POST.get("salle_de_sport", "non") == "oui",
            "aire_de_jeux": request.POST.get("aire_de_jeux", "non") == "oui",
        }
        services = {
            "nettoyage_a_sec": request.POST.get("nettoyage_a_sec", "non") == "oui",
            "service_de_chambre": request.POST.get("service_de_chambre", "non")
            == "oui",
            "service_special": request.POST.get("service_special", "non") == "oui",
            "aire_dattente": request.POST.get("aire_dattente", "non") == "oui",
            "concierge": request.POST.get("concierge", "non") == "oui",
            "service_de_repassage": request.POST.get("service_de_repassage", "non")
            == "oui",
            "wifi_gratuit": request.POST.get("wifi_gratuit", "non") == "oui",
            "ascenseur": request.POST.get("ascenseur", "non") == "oui",
        }
        reception_evenements = {
            "reception_evenements": request.POST.get("reception_evenements", "non")
            == "oui",
            "salle_conference": request.POST.get("salle_conference", "non") == "oui",
            "salle_reunion": request.POST.get("salle_reunion", "non") == "oui",
            "equipement_audiovisuel": request.POST.get("equipement_audiovisuel", "non")
            == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        for prestation in prestations:
            prestation.activites = activites
            prestation.services = services
            prestation.reception_evenements = reception_evenements
            prestation.langues_personnel = langues_personnel
            prestation.methodes_paiement = methodes_paiement
            prestation.save()

        messages.success(
            request, f" la prestation de l'hôtel {hotel.nom} a été modifié avec succès."
        )

        return redirect("listeHotel")

    hotels = Hotel.objects.all()
    context = {
        "hotels": hotels,
        "prestations": prestations,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-modifierPrestationHotel.html", context)


# Restauration


def ajouterRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    context = {
        "pays": pays,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        # Récupérer les données du restaurant
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        adresse = request.POST.get("adresse")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        coordonnees_tel = request.POST.get("coordonnees_tel")
        nombre_de_tables = request.POST.get("nombre_de_tables")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        # Créer l'objet restaurant
        restaurant = Restaurant.objects.create(
            nom=nom,
            description=description,
            statut=statut,
            adresse=adresse,
            ville=ville,
            pays=pays,
            coordonnees_tel=coordonnees_tel,
            nombre_de_tables=nombre_de_tables,
            photo=first_photo,
        )

        # Récupérer et associer les photos
        photos = request.FILES.getlist("images")
        for photo in photos:
            PhotoRestaurant.objects.create(image=photo, restaurant=restaurant)

        return redirect("listeRestaurant")
    else:
        return render(request, "frontend/admin-ajouterRestaurant.html", context)


def listeRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    restaurants = Restaurant.objects.all()
    restaurants_with_min_price = []

    for restaurant in restaurants:
        # Filtre les menus par type "plat principal" et calcule le prix minimum
        min_price_menu = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).aggregate(min_prix=Min("prix"))
        
        # Récupère le prix minimum
        min_price = min_price_menu["min_prix"]

        # Vérifie s'il y a au moins un menu de type "plat principal"
        has_main_dish = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).exists()
        
        # Vérifie s'il y a au moins un menu de n'importe quel type
        has_any_menu = Menu.objects.filter(
            restaurant=restaurant
        ).exists()

        # Ajoute le restaurant et son prix minimum à la liste, ainsi que l'indicateur de plat principal
        restaurants_with_min_price.append(
            {
                "restaurant": restaurant, 
                "min_price": min_price, 
                "has_main_dish": has_main_dish,
                "has_any_menu": has_any_menu
            }
        )

    context = {
        "restaurants_with_min_price": restaurants_with_min_price,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }
    return render(request, "frontend/admin-listeRestaurant.html", context)


def modifierRestaurant(request, restaurant_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    pays = [
    "Bénin","Burkina Faso","Côte d'Ivoire","Ghana",
	"Guinée","Guinée-Bissau","Liberia",
	"Mali","Sénégal","Togo",
]

    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    if request.method == "POST":
        restaurant.nom = request.POST.get("nom")
        restaurant.description = request.POST.get("description")
        restaurant.statut = request.POST.get("statut")
        restaurant.adresse = request.POST.get("adresse")
        restaurant.ville = request.POST.get("ville")
        restaurant.pays = request.POST.get("pays")
        restaurant.coordonnees_tel = request.POST.get("coordonnees_tel")
        restaurant.nombre_de_tables = request.POST.get("nombre_de_tables")

        if request.FILES.get("photo"):
            restaurant.photo = request.FILES.get("photo")

        restaurant.save()
        messages.success(
            request, f"Le restaurant '{restaurant.nom}' a été mise à jour avec succès."
        )
        return redirect("listeRestaurant")

    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "restaurant": restaurant,
        "pays": pays,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-modifierRestaurant.html", context)


def supprimerRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    photos_restaurant = Photo.objects.filter(restaurant=restaurant)
    menus = Menu.objects.filter(menu=menu)

    for menu in menus:
        photos_menu = PhotoMenu.objects.filter(menu=menu)
        photos_menu.delete()

    photos_restaurant.delete()
    menu.delete()
    restaurant.delete()

    messages.success(
        request, f"Le restaurant {restaurant.nom} a été supprimée avec succès."
    )

    return redirect("listeRestaurant")


def detailRestaurant(request, restaurant_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)
    photos = PhotoRestaurant.objects.filter(restaurant=restaurant)
    menu_avec_prix_minimal = (
        Menu.objects.filter(restaurant=restaurant).order_by("prix").first()
    )
    context = {
        "restaurant": restaurant,
        "prestations": prestations,
        "photos": photos,
        "menu_avec_prix_minimal": menu_avec_prix_minimal,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
    }

    return render(request, "frontend/admin-detailRestaurant.html", context)


def ajouterMenu(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        restaurant_id = request.POST.get("restaurant")
        type_de_plat = request.POST.get("type_de_plat")
        prix = request.POST.get("prix")

        # Récupérer la première photo de la liste
        photos = request.FILES.getlist("images")
        if photos:
            first_photo = photos[0]
        else:
            first_photo = None

        restaurant = Restaurant.objects.get(id=restaurant_id)

        menu = Menu.objects.create(
            nom=nom,
            description=description,
            restaurant=restaurant,
            type_de_plat=type_de_plat,
            prix=prix,
            photo=first_photo,
        )

        photos = request.FILES.getlist("images")
        for photo in photos:
            PhotoMenu.objects.create(image=photo, menu=menu)

        return redirect("listeMenu")

    return render(request, "frontend/admin-ajouterMenu.html", context)


def listeMenu(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    menus = Menu.objects.all()
    context = {
        "menus": menus,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-listeMenu.html", context)


def supprimerMenu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    photos = PhotoMenu.objects.filter(menu=menu)

    photos.delete()
    menu.delete()

    messages.success(request, f"Le menu '{menu.nom}'a été supprimée avec succès.")

    return redirect("listeMenu")


def modifierMenu(request, menu_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    menu = get_object_or_404(Menu, pk=menu_id)

    if request.method == "POST":
        
        menu.nom = request.POST.get("nom")
        menu.description = request.POST.get("description")
        menu.restaurant_id = request.POST.get("restaurant")
        menu.type_de_plat = request.POST.get("type_de_plat")
        menu.prix = float(
            request.POST.get("prix").replace(",", ".").replace("\xa0", "")
        )

        menu.restaurant_id = request.POST.get("restaurant")

        if request.FILES.get("photo"):
            menu.photo = request.FILES.get("photo")

        menu.save()
        messages.success(request, f"Le menu'{menu.nom}' a été mise à jour avec succès.")
        return redirect("listeMenu")

    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "menu": menu,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-modifierMenu.html", context)


def detailMenu(request, menu_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    menu = get_object_or_404(Menu, pk=menu_id)
    photos = PhotoMenu.objects.filter(menu=menu)
    
    context = {
        "menu": menu,
        "photos": photos,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-detailMenu.html", context)


def ajouterPrestationRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant")
        services = {
            "diners_avec_spectacle": request.POST.get("diners_avec_spectacle", "non") == "oui",
            "soirees_a_theme": request.POST.get("soirees_a_theme", "non") == "oui",
            "menus_degustation": request.POST.get("menus_degustation", "non") == "oui",
            "diners_prives": request.POST.get("diners_prives", "non") == "oui",
            "programmes_de_fidelite": request.POST.get("programmes_de_fidelite", "non") == "oui",
            "anniversaire": request.POST.get("anniversaire", "non") == "oui",
        }

        types_de_cuisine  = {
            "mexicaine": request.POST.get("mexicaine", "non") == "oui",
            "chinoise": request.POST.get("chinoise", "non") == "oui",
            "japonaise": request.POST.get("japonaise", "non") == "oui",
            "française": request.POST.get("française", "non") == "oui",
            "africaine": request.POST.get("africaine", "non") == "oui",
            "autres": request.POST.get("autres", "non") == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        prestations = PrestationRestaurant(
            restaurant=restaurant,
            services=services,
            types_de_cuisine=types_de_cuisine,
            langues_personnel=langues_personnel,
            methodes_paiement=methodes_paiement,
        )
        prestations.save()

        messages.success(
            request, f"La prestation du restaurant '{restaurant.nom}' a été ajouter avec succès."
        )
        return redirect("listeRestaurant")

    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-ajouterPrestationRestaurant.html", context)



def supprimerPrestationRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)

    prestations.delete()

    messages.success(
        request,
        f" la prestation du restaurant '{restaurant.nom}' a été supprimée avec succès.",
    )

    return redirect("listeRestaurant")


def modifierPrestationRestaurant(request, restaurant_id):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Ajoutez cette ligne pour récupérer le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    prestations = PrestationRestaurant.objects.filter(restaurant=restaurant)

    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant")
        services = {
            "diners_avec_spectacle": request.POST.get("diners_avec_spectacle", "non") == "oui",
            "soirees_a_theme": request.POST.get("soirees_a_theme", "non") == "oui",
            "menus_degustation": request.POST.get("menus_degustation", "non") == "oui",
            "diners_prives": request.POST.get("diners_prives", "non") == "oui",
            "programmes_de_fidelite": request.POST.get("programmes_de_fidelite", "non") == "oui",
            "anniversaire": request.POST.get("anniversaire", "non") == "oui",
        }

        types_de_cuisine  = {
            "mexicaine": request.POST.get("mexicaine", "non") == "oui",
            "chinoise": request.POST.get("chinoise", "non") == "oui",
            "japonaise": request.POST.get("japonaise", "non") == "oui",
            "française": request.POST.get("française", "non") == "oui",
            "africaine": request.POST.get("africaine", "non") == "oui",
            "autres": request.POST.get("autres", "non") == "oui",
        }
        langues_personnel = {
            "anglais": request.POST.get("anglais", "non") == "oui",
            "espagnol": request.POST.get("espagnol", "non") == "oui",
            "francais": request.POST.get("francais", "non") == "oui",
            "allemand": request.POST.get("allemand", "non") == "oui",
        }
        methodes_paiement = {
            "carte_de_credit": request.POST.get("carte_de_credit", "non") == "oui",
            "especes": request.POST.get("especes", "non") == "oui",
            "carte_de_debit": request.POST.get("carte_de_debit", "non") == "oui",
            "mobile_money": request.POST.get("mobile_money", "non") == "oui",
        }

        for prestation in prestations:
            prestation.services = services
            prestation.types_de_cuisine  = types_de_cuisine
            prestation.langues_personnel = langues_personnel
            prestation.methodes_paiement = methodes_paiement
            prestation.save()

        messages.success(
            request,
            f" la prestation du restaurant '{restaurant.nom}' a été modifié avec succès.",
        )

        return redirect("listeRestaurant")

    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "prestations": prestations,
        'username': username,
        'user_avatar_url' : user_avatar_url,
        'user_email'  :  user_email,
        }

    return render(request, "frontend/admin-modifierPrestationRestaurant.html", context)



#validation liste Hotel
def validation_listeHotel(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    hotels_valides = Hotel.objects.filter(is_validated=True)
        
    # Filtrer les hôtels qui ont au moins une chambre et une prestation
    hotels_with_min_price = Hotel.objects.annotate(
        min_price=Min('chambres__tarif_par_nuit')
    ).filter(
        chambres__isnull=False, 
        prestations__isnull=False
    ).distinct()
    
    context = {
        "hotels_with_min_price": hotels_with_min_price,
        'username': username,
        'user_avatar_url': user_avatar_url,
        'user_email': user_email,
        'hotels_valides': hotels_valides,
    }
    return render(request, "frontend/admin-validation-listeHotel.html", context)


#Validation accepter hotel
def validation_accepter_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    hotel.is_validated = True
    hotel.save()
    
    messages.success(request, f"L'hôtel '{hotel.nom}' a été accepté.")
    return redirect('validation-listeHotel')

#validation refuser hotel
def validation_refuser_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    hotel.delete()
    messages.success(request, f"L'hôtel '{hotel.nom}' a été refusé et supprimé.")
    return redirect('validation-listeHotel')


#validation liste Restaurant
def validation_listeRestaurant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')  # Récupère le nom d'utilisateur
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
    
    restaurants_valides = Restaurant.objects.filter(is_validated=True)
    restaurants_non_valides = Restaurant.objects.filter(is_validated=False)
    
    restaurants = Restaurant.objects.all()
    restaurants_with_min_price = []

    for restaurant in restaurants:
        # Vérifie s'il y a au moins un menu de type "plat principal"
        has_main_dish = Menu.objects.filter(
            restaurant=restaurant, type_de_plat="plat principal"
        ).exists()

        # Vérifie s'il y a au moins une prestation
        has_any_prestation = PrestationRestaurant.objects.filter(restaurant=restaurant).exists()

        if has_main_dish and has_any_prestation:
            # Filtre les menus par type "plat principal" et calcule le prix minimum
            min_price_menu = Menu.objects.filter(
                restaurant=restaurant, type_de_plat="plat principal"
            ).aggregate(min_prix=Min("prix"))
            
            # Récupère le prix minimum
            min_price = min_price_menu["min_prix"]

            # Ajoute le restaurant et son prix minimum à la liste, ainsi que l'indicateur de plat principal
            restaurants_with_min_price.append(
                {
                    "restaurant": restaurant, 
                    "min_price": min_price, 
                    "has_main_dish": has_main_dish,
                }
            )

    context = {
        "restaurants_with_min_price": restaurants_with_min_price,
        'username': username,
        'user_avatar_url': user_avatar_url,
        'user_email': user_email,
        'restaurants_valides': restaurants_valides,
        'restaurants_non_valides': restaurants_non_valides,
    }
    return render(request, "frontend/admin-validation-listeRestaurant.html", context)


#Validation accepter restaurant
def validation_accepter_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    restaurant.is_validated = True
    restaurant.save()
    
    messages.success(request, f"Le restaurant '{restaurant.nom}' a été accepté.")
    return redirect('validation-listeRestaurant')

#Validation refuser restaurant
def validation_refuser_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    restaurant.delete()
    messages.success(request, f"Le restaurant '{restaurant.nom}' a été refusé et supprimé.")
    return redirect('validation-listeRestaurant')



#validation liste Gérant
def validation_listeGerant(request):
    user_email = request.session.get('user_email')
    username = request.session.get('username')
    user_avatar_url = None
    if user_email:
        email_hash = hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()
        user_avatar_url = f"https://www.gravatar.com/avatar/{email_hash}"
        
    gerants = Gerant.objects.all()
    documentsGerant = DocumentGerant.objects.all()

    
    context = {
        "gerants": gerants,
        'username': username,
        'user_avatar_url': user_avatar_url,
        'user_email': user_email,
        'documentsGerant': documentsGerant,
    }
    return render(request, "frontend/admin-validation-listeGerant.html", context)


#Validation accepter gérant
def validation_accepter_gerant(request, gerant_id):
    gerant = get_object_or_404(Gerant, pk=gerant_id)
    gerant.is_validated = True
    gerant.save()
    
    messages.success(request, f"L'utilisateur '{gerant.nom} {gerant.prenom}' a été accepté comme gérant.")
    return redirect('validation-listeGerant')

#validation refuser gérant
def validation_refuser_gerant(request, gerant_id):
    gerant = get_object_or_404(Gerant, pk=gerant_id)
    gerant.delete()
    messages.success(request, f"L'utilisateur '{gerant.nom} {gerant.prenom}' a été refusé comme gérant.")
    return redirect('validation-listeGerant')
