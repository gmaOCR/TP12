# TP12 - Développez une architecture back-end sécurisée en utilisant Django ORM

TP12 d'openClassRoom - Créer un CRM sécurisé interne à une entreprise. Développer un API en utilisant une base PostgreSQL + Django REST. Utiliser l'interface web de django-admin pour administrer l'utilisation.

## Présentation
L'applicatif est basé sur 3 groupes d'utilisateurs: *vente*, *support* et *gestion*.
- *gestion* est le groupe des super-user
- *vente* et *support* sont les groupes d'utilisateurs principaux du produit

En fonction des droits prédéfinis pour chacun de ces groupes, les utilisateurs agiront sur des `#0969DA` *Clients*, *Contracts* et *events*.

## Installation

Utiliser [pip](https://pip.pypa.io/en/stable/) pour installer les dépendances.

Clonez le projet:
```bash
git clone https://github.com/gmaOCR/TP12.git
```
Contrôler l'installation de pipenv:
```bash
pip install --user pipenv
```
Installer pipenv et les dépendances:
```bash
pipenv install
```
Activez l'environnement virtuel:
```bash
pipenv shell
```
Lancez le serveur:
```bash 
python manage.py runserver
```
---
## Documentation de l'API

La documentation des requêtes et de l'API sont disponibles [ici](https://documenter.getpostman.com/view/24264370/2s93XsY6FX)

---
## License
[GNU](https://choosealicense.com/licenses/gpl-2.0/)