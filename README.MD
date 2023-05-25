# TP12 - Développez une architecture back-end sécurisée en utilisant Django ORM

TP12 d'openClassRoom - Créer un CRM sécurisé interne à une entreprise. Développer un API en utilisant une base PostgreSQL + Django REST. Utiliser l'interface web de django-admin pour administrer l'utilisation.

## Présentation
L'applicatif est basé sur 3 groupes d'utilisateurs: *vente*, *support* et *gestion*.
- *gestion* est le groupe des super-user
- *vente* et *support* sont les groupes d'utilisateurs principaux du produit

En fonction des droits prédéfinis pour chacun de ces groupes, les utilisateurs agiront sur des *Clients*, *Contracts* et/ou *Events*.

## Installation

Utiliser [pip](https://pip.pypa.io/en/stable/) pour installer les dépendances.

Clonez le projet:
```bash
git clone https://github.com/gmaOCR/TP12.git
cd TP12
```
(Contrôler l'installation de pipenv:)
```bash
(pip install --user pipenv)
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
cd epicEvents
python manage.py runserver
```
---
## Documentation de l'API

La documentation des requêtes et de l'API sont disponibles [ici](https://documenter.getpostman.com/view/24264370/2s93m4X2dB)
Les endpoints des recherches sont détaillés sur cette documentation

---
## License
[GNU](https://choosealicense.com/licenses/gpl-2.0/)