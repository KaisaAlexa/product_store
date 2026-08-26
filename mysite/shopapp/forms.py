from django import forms
from .models import Product


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(file, initial) for file in data]
        return single_clean(data, initial)


class ProductForm(forms.ModelForm):
    images = MultipleImageField(required=False)

    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount", "preview")


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
