from django import forms


class AddEmailForm(forms.Form):
  email = forms.EmailField(max_length=200)
