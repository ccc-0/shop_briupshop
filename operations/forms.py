from django import forms

class AddAddressForm(forms.Form):
    name = forms.CharField(required=True)
    detailedaddress = forms.CharField(required=True)
    zipcode = forms.IntegerField()
    tel = forms.CharField()

