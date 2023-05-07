from django import forms
from django.core.exceptions import ValidationError
from django.forms import HiddenInput

from .models import Client, Contract, Event
from authentication.models import User


class ClientForm(forms.ModelForm):
    edit_client = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'sales_contact']
        widgets = {
            'sales_contact': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sales_contact'].queryset = User.objects.filter(role='vente')

    def clean_sales_contact(self):
        sales_contact = self.cleaned_data['sales_contact']
        if sales_contact.role != 'vente':
            raise forms.ValidationError("Le contact de vente sélectionné n'a pas le rôle 'Vente'")
        return sales_contact


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['status', 'client', 'amount', 'paymentDue']

    status = forms.BooleanField(required=False, label='Signé ?')
    client = forms.ModelChoiceField(queryset=Client.objects.all(), to_field_name='client_id',
                                    label='Client', widget=forms.Select(attrs={'class': 'form-control'}))
    sales_contact = forms.ModelChoiceField(required=False, queryset=User.objects.none(), widget=HiddenInput())
    amount = forms.FloatField(required=False, label='Montant du contrat')
    paymentDue = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Paiement dû le')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['sales_contact'].queryset = User.objects.filter(username=instance.client.sales_contact.username)

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        if client and not client.sales_contact:
            raise ValidationError("Le client sélectionné n'a pas de contact de vente")
        if client and client.sales_contact:
            cleaned_data['sales_contact'] = client.sales_contact
        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['client', 'eventStatus', 'attendes', 'eventDate', 'note']
        widgets = {
            'eventDate': forms.DateInput(attrs={'type': 'date'})
        }

class DeleteForm(forms.Form):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)
