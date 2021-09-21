from django import forms
from .models import Product, Sizes


class AddSizeForm(forms.Form):
    size = forms.ModelChoiceField(queryset=None)
    quantity = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        self.product_pk = kwargs.pop('pk', None)
        super(AddSizeForm, self).__init__(*args, **kwargs)
        product = Product.objects.get(pk=self.product_pk)
        self.fields['size'].queryset = product.sizes_set.all()


