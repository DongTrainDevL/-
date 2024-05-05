from django import forms

class CartForm(forms.Form):
    food_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1)

