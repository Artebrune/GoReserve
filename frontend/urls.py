from django.urls import path 
from .import views
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import signup_user, logout_user, login_user

urlpatterns = [ 
               
    #Users accueil
    path('accueil', views.accueil, name='accueil'),
    
    #Users profile
    path('user-mesReservations', views.user_mesReservations, name='user-mesReservations'),
    
    #Users Hotel
    path('user-listeHotel', views.user_listeHotel, name='user-listeHotel'),
    path('user-detailHotel/<int:hotel_id>/', views.user_detailHotel, name='user-detailHotel'),
    path('user-admin-listeReservationHotels', views.user_admin_listeReservationHotels, name='user-admin-listeReservationHotels'),
    path('validation-accepter-reservation-hotel/<int:reservation_id>/', views.validation_accepter_reservation_hotel, name='validation-accepter-reservation-hotel'),
    path('validation-refuser-reservation-hotel/<int:reservation_id>/', views.validation_refuser_reservation_hotel, name='validation-refuser-reservation-hotel'),
    path('user-paiement-hotel/<int:reservation_id>/', views.user_paiement_hotel, name='user-paiement-hotel'),
    
    #Users Restaurant
    path('user-listeRestaurant', views.user_listeRestaurant, name='user-listeRestaurant'),
    path('user-detailRestaurant/<int:restaurant_id>/', views.user_detailRestaurant, name='user-detailRestaurant'),
    path('user-admin-listeReservationRestaurants', views.user_admin_listeReservationRestaurants, name='user-admin-listeReservationRestaurants'),
    path('validation-accepter-reservation-Restaurant/<int:reservation_id>/', views.validation_accepter_reservation_restaurant, name='validation-accepter-reservation-restaurant'),
    path('validation-refuser-reservation-Restaurant/<int:reservation_id>/', views.validation_refuser_reservation_restaurant, name='validation-refuser-reservation-restaurant'),
    
    #Users reserver restaurant
    path('user-reserverRestaurant/<int:restaurant_id>/', views.user_reserverRestaurant, name='user-reserverRestaurant'),
    path('user-confirmerReservationRestaurant/<int:reservation_id>/', views.user_confirmerReservationRestaurant, name='user-confirmerReservationRestaurant'),
    path('user-annulerReservationRestaurant/<int:reservation_id>/', views.user_annulerReservationRestaurant, name='user-annulerReservationRestaurant'),
    #Paiement
    path('user-paiement-restaurant/<int:reservation_id>/', views.user_paiement_restaurant, name='user-paiement-restaurant'),
    
    #Users reserver chambre
    path('user-reserverChambre/<int:chambre_id>/', views.user_reserverChambre, name='user-reserverChambre'),
    path('user-confirmerReservationChambre/<int:reservation_id>/', views.user_confirmerReservationChambre, name='user-confirmerReservationChambre'),
    path('user-annulerReservationChambre/<int:reservation_id>/', views.user_annulerReservationChambre, name='user-annulerReservationChambre'),
    
   
   #Users-admin
    path('devenirPrestataire', views.devenirPrestataire, name='devenirPrestataire'),
    path('user-dash-admin', views.user_dash_admin, name='user-dash-admin'),
    path('user-admin-ajouterChambre', views.user_admin_ajouterChambre, name='user-admin-ajouterChambre'),
    path('user-admin-listeChambre', views.user_admin_listeChambre, name='user-admin-listeChambre'),
    path('user-admin-detailChambre/<int:chambre_id>/', views.user_admin_detailChambre, name='user-admin-detailChambre'),
    path('user-admin-modifierChambre/<int:chambre_id>/', views.user_admin_modifierChambre, name='user-admin-modifierChambre'),
    path('user-admin-supprimerChambre/<int:chambre_id>/', views.user_admin_supprimerChambre, name='user-admin-supprimerChambre'),
    
    
    path('user-admin-ajouterHotel', views.user_admin_ajouterHotel, name='user-admin-ajouterHotel'),
    path('user-admin-listeHotel', views.user_admin_listeHotel, name='user-admin-listeHotel'),
    path('user-admin-detailHotel/<int:hotel_id>/', views.user_admin_detailHotel, name='user-admin-detailHotel'),
    path('user-admin-modifierHotel/<int:hotel_id>/', views.user_admin_modifierHotel, name='user-admin-modifierHotel'),
    path('user-admin-supprimerHotel/<int:hotel_id>/', views.user_admin_supprimerHotel, name='user-admin-supprimerHotel'),
    
    path('user-admin-ajouterPrestationHotel', views.user_admin_ajouterPrestationHotel, name='user-admin-ajouterPrestationHotel'),
    path('user-admin-supprimerPrestationHotel/<int:hotel_id>/', views.user_admin_supprimerPrestationHotel, name='user-admin-supprimerPrestationHotel'),
    path('user-admin-modifierPrestationHotel/<int:hotel_id>/', views.user_admin_modifierPrestationHotel, name='user-admin-modifierPrestationHotel'),
    
    
    path('user-admin-ajouterRestaurant', views.user_admin_ajouterRestaurant, name='user-admin-ajouterRestaurant'),
    path('user-admin-listeRestaurant', views.user_admin_listeRestaurant, name='user-admin-listeRestaurant'),
    path('user-admin-detailRestaurant/<int:restaurant_id>/', views.user_admin_detailRestaurant, name='user-admin-detailRestaurant'),
    path('user-admin-supprimerRestaurant/<int:restaurant_id>/', views.user_admin_supprimerRestaurant, name='user-admin-supprimerRestaurant'),
    path('user-admin-modifierRestaurant/<int:restaurant_id>/', views.user_admin_modifierRestaurant, name='user-admin-modifierRestaurant'),
    
    path('user-admin-ajouterMenu', views.user_admin_ajouterMenu, name='user-admin-ajouterMenu'),
    path('user-admin-listeMenu', views.user_admin_listeMenu, name='user-admin-listeMenu'),
    path('user-admin-supprimerMenu/<int:menu_id>/', views.user_admin_supprimerMenu, name='user-admin-supprimerMenu'),
    path('user-admin-modifierMenu/<int:menu_id>/', views.user_admin_modifierMenu, name='user-admin-modifierMenu'),
    
    
    path('user-admin-ajouterPrestationRestaurant', views.user_admin_ajouterPrestationRestaurant, name='user-admin-ajouterPrestationRestaurant'),
    path('user-admin-supprimerPrestationRestaurant/<int:restaurant_id>/', views.user_admin_supprimerPrestationRestaurant, name='user-admin-supprimerPrestationRestaurant'),
    path('user-admin-modifierPrestationRestaurant/<int:restaurant_id>/', views.user_admin_modifierPrestationRestaurant, name='user-admin-modifierPrestationRestaurant'),
    
    #Authentification
    path('', login_user, name='login'),
    path('inscription', signup_user, name='signup'),
    path('logout', logout_user, name='logout'),
    

    
    
    #Hotellerie
    path('dashboard', views.dashboard, name='dashboard'),
    path('base', views.base, name='base'),
    
    path('ajouterHotel', views.ajouterHotel, name='ajouterHotel'),
    path('listeHotel', views.listeHotel, name='listeHotel'),
    path('supprimerHotel/<int:hotel_id>/', views.supprimerHotel, name='supprimerHotel'),
    path('modifierHotel/<int:hotel_id>/', views.modifierHotel, name='modifierHotel'),
    path('detailHotel/<int:hotel_id>/', views.detailHotel, name='detailHotel'),
    
    path('ajouterChambre', views.ajouterChambre, name='ajouterChambre'),
    path('listeChambre', views.listeChambre, name='listeChambre'),
    path('supprimerChambre/<int:chambre_id>/', views.supprimerChambre, name='supprimerChambre'),
    path('modifierChambre/<int:chambre_id>/', views.modifierChambre, name='modifierChambre'),
    path('detailChambre/<int:chambre_id>/', views.detailChambre, name='detailChambre'),
    
    path('ajouterPrestationHotel', views.ajouterPrestationHotel, name='ajouterPrestationHotel'),
    path('supprimerPrestationHotel/<int:hotel_id>/', views.supprimerPrestationHotel, name='supprimerPrestationHotel'),
    path('modifierPrestationHotel/<int:hotel_id>/', views.modifierPrestationHotel, name='modifierPrestationHotel'),
    
    
    
    #Restauration
    path('ajouterRestaurant', views.ajouterRestaurant, name='ajouterRestaurant'),
    path('listeRestaurant', views.listeRestaurant, name='listeRestaurant'),
    path('supprimerRestaurant/<int:restaurant_id>/', views.supprimerRestaurant, name='supprimerRestaurant'),
    path('modifierRestaurant/<int:restaurant_id>/', views.modifierRestaurant, name='modifierRestaurant'),
    path('detailRestaurant/<int:restaurant_id>/', views.detailRestaurant, name='detailRestaurant'),
    
    path('ajouterMenu', views.ajouterMenu, name='ajouterMenu'),
    path('listeMenu', views.listeMenu, name='listeMenu'),
    path('supprimerMenu/<int:menu_id>/', views.supprimerMenu, name='supprimerMenu'),
    path('modifierMenu/<int:menu_id>/', views.modifierMenu, name='modifierMenu'),
    path('detailMenu/<int:menu_id>/', views.detailMenu, name='detailMenu'),
    
    path('ajouterPrestationRestaurant', views.ajouterPrestationRestaurant, name='ajouterPrestationRestaurant'),
    path('supprimerPrestationRestaurant/<int:restaurant_id>/', views.supprimerPrestationRestaurant, name='supprimerPrestationRestaurant'),
    path('modifierPrestationRestaurant/<int:restaurant_id>/', views.modifierPrestationRestaurant, name='modifierPrestationRestaurant'),

    
    #Validation 
    #Hôtels
    path('validation-listeHotel', views.validation_listeHotel, name='validation-listeHotel'),
    path('validation-accepter-hotel/<int:hotel_id>/', views.validation_accepter_hotel, name='validation-accepter-hotel'),
    path('validation-refuser-hotel/<int:hotel_id>/', views.validation_refuser_hotel, name='validation-refuser-hotel'),
    
    #restaurants
    path('validation-listeRestaurant', views.validation_listeRestaurant, name='validation-listeRestaurant'),
    path('validation-accepter-restaurant/<int:restaurant_id>/', views.validation_accepter_restaurant, name='validation-accepter-restaurant'),
    path('validation-refuser-restaurant/<int:restaurant_id>/', views.validation_refuser_restaurant, name='validation-refuser-restaurant'),
    
    #Gérant
    path('validation-listeGerant', views.validation_listeGerant, name='validation-listeGerant'),
    path('validation-accepter-gerant/<int:gerant_id>/', views.validation_accepter_gerant, name='validation-accepter-gerant'),
    path('validation-refuser-gerant/<int:gerant_id>/', views.validation_refuser_gerant, name='validation-refuser-gerant'),
    
    
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)