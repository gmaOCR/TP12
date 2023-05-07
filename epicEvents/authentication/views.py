from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})



# def home(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('clients')  # remplacez 'menu-utilisateur' par l'URL de votre page de menu utilisateur
#     else:
#         form = AuthenticationForm()
#     return render(request, 'authentication/home.html', {'form': form})
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('home')


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
