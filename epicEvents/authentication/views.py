from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('clients')  # remplacez 'menu-utilisateur' par l'URL de votre page de menu utilisateur
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/home.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# @login_required
# def menu(request):
#     if request.user.is_superuser:
#         links = [
#             {'name': 'Page d\'administration', 'url': '/admin/'},
#             {'name': 'Déconnexion', 'url': '/logout/'}
#         ]
#     elif request.user.role == 'Vente':
#         links = [
#             {'name': 'Liste des ventes', 'url': '/ventes/'},
#             {'name': 'Déconnexion', 'url': '/logout/'}
#         ]
#     elif request.user.role == 'Support':
#         links = [
#             {'name': 'Demandes de support', 'url': '/support/'},
#             {'name': 'Déconnexion', 'url': '/logout/'}
#         ]
#     elif request.user.role == 'Gestion':
#         links = [
#             {'name': 'Demandes de support', 'url': '/Gestion/'},
#             {'name': 'Déconnexion', 'url': '/logout/'}
#         ]
#     else:
#         links = [{'name': 'Déconnexion', 'url': '/logout/'}]
#     return render(request, 'authentication/menu.html', {'links': links})

