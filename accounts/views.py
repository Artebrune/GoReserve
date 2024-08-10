from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model , login, logout, authenticate
from django.contrib import messages

User = get_user_model()

def signup_user(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        Confirmpassword = request.POST['Confirmpassword']
        #Vérification d'un existence avec le meme nom d'utilisateur
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Un utilisateur avec le même nom d\'utilisateur existe déjà.')
            return redirect('signup')
         # Vérification que les mots de passe correspondent
        if password != Confirmpassword:
            messages.error(request, f"Les mots de passe ne correspondent pas.")
            return redirect('signup')

        # Si les mots de passe correspondent, procédez à l'enregistrement de l'utilisateur

        _ = User.objects.create_user(email=email, username=username,password=password)
        messages.success(request, 'Votre compte a été créé avec succès.')
        return redirect('login')
    return render(request, 'inscription.html')


def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)

            # Connexion réussie, stocker les informations dans la session       
        if user:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username  # Stocker le nom d'utilisateur dans la session
            request.session['user_email'] = user.email  # Vous pouvez aussi stocker l'email si nécessaire
            return redirect('accueil')
        else:
            messages.error(request, f"Nom d\'utilisateur ou mot de passe incorrect.")
            return redirect('login')
    return render(request, 'connexion.html')


def logout_user(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'username' in request.session:
        del request.session['username']
    if 'user_email' in request.session:
        del request.session['user_email']
    logout(request)
    return redirect('login')


def user_logged_in(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Remplacez 'nom_de_votre_vue_accueil' par le nom de votre vue d'accueil
    return wrapper_func
