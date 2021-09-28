from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='', max_value=9, min_value=1)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
