from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(DjangoUserAdmin):
    # Affichage du menu de base User
    list_display = ('username', 'role', 'first_name', 'last_name', 'is_superuser')
    # Spécifiez les champs à afficher lors de l'ajout d'un utilisateur
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),

        }),
    )

    # Spécifiez les champs à afficher lors de la modification d'un utilisateur
    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        })
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        instance = form.instance
        # Vérifiez si l'utilisateur est un superutilisateur
        if not instance.is_superuser:
            if instance.groups.exists():
                group = instance.groups.first()
                if group.name == 'vente':
                    instance.role = 'vente'
                elif group.name == 'support':
                    instance.role = 'support'
            else:
                instance.role = 'support'
            instance.save()
        else:
            instance.role = 'gestion'
            instance.save()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
