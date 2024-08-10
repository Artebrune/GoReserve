from django.urls import path 
from .import views


urlpatterns = [ 
    #Authentification
    path('', views.login_user, name='login'),
    path('inscription', views.signup_user, name='signup'),
    path('logout', views.logout_user, name='logout'),
]  
  