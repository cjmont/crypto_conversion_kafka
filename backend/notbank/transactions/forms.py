from django import forms

from notbank.transactions.models import Transfer


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
