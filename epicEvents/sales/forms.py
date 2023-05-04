from django import forms
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
        fields = ['sales_contact', 'client', 'amount', 'paymentDue']

    sales_contact = forms.ModelChoiceField(queryset=User.objects.all())
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    amount = forms.FloatField(required=False)
    paymentDue = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_sales_contact(self):
        sales_contact = self.cleaned_data['sales_contact']
        if sales_contact.role != 'vente':
            raise forms.ValidationError("Le contact de vente sélectionné n'a pas le rôle 'Vente'")
        return sales_contact


class DeleteForm(forms.Form):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)