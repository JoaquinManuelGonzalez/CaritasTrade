from django import forms


from django import forms
from django.core.exceptions import ValidationError
from data_base.models import ProductCategory


class ExchangeForm(forms.Form):
    title = forms.CharField(
        label="Titulo",
        error_messages={
            "required": "Ingresar el titulo de la publicacion, por favor",
            "invalid": "Ingresar el titulo de la publicacion, por favor",
        },
    )
    description = forms.CharField(label="Descripcion",
        error_messages={
            "required": "Ingresar la descripcion de la publicacion, por favor",
            "invalid": "Ingresar la descripcion de la publicacion, por favor",
        },)
    image = forms.ImageField(label="Imagen", required=False,
        error_messages={
            "required": "Ingresar el titulo de la publicacion, por favor",
            "invalid": "Ingresar el titulo de la publicacion, por favor",
        },)
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(), label="Categoria",
        error_messages={
            "required": "Seleccionar la categoria de la publicacion, por favor",
            "invalid": "Seleccionar la categoria de la publicacion, por favor",
        },
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 20:
            raise ValidationError(
                "El titulo es erroneo, debe ser menor a 20 caracteres"
            )
        return title.lower().capitalize()

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) > 300:
            raise ValidationError(
                "Ingresar la descripcion de la publicacion, por favor"
            )
        return description

    def clean_category(self):
        category = self.cleaned_data.get("category")
        if not category:
            raise ValidationError(
                "Seleccionar la categoria de la publicacion, por favor"
            )
        return category
