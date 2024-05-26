from django import forms


from django import forms
from django.core.exceptions import ValidationError
from data_base.models import ProductCategory


class ExchangeForm(forms.Form):
    """
    Defines a Django form for creating an exchange post.

    The `ExchangeForm` class inherits from `forms.Form` and defines the following fields:

    - `title`: A `CharField` for the title of the post, with a maximum length of 20 characters and custom error messages.
    - `description`: A `CharField` for the description of the post, with a maximum length of 300 characters and custom error messages.
    - `image`: An `ImageField` for the post's image, which is optional.
    - `category`: A `ModelChoiceField` for selecting the category of the post, with custom error messages.

    The form also includes custom clean methods for the `title`, `description`, and `category` fields to perform additional validation and formatting.
    """

    title = forms.CharField(
        label="Titulo",
        max_length=20,
        error_messages={
            "required": "Ingresar el titulo de la publicacion, por favor",
            "max_length": "El titulo es erroneo, debe ser menor a 20 caracteres",
        },
    )
    description = forms.CharField(
        label="Descripcion",
        max_length=300,
        error_messages={
            "required": "Ingresar la descripcion de la publicacion, por favor",
            "max_length": "El titulo es erroneo, debe ser menor a 300 caracteres",
        },
    )
    image = forms.ImageField(
        label="Imagen",
        required=False,
        error_messages={
            "invalid": "La imagen es invalida, ingrese otra por favor",
        },
    )
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        label="Categoria",
        error_messages={
            "required": "Seleccionar la categoria de la publicacion, por favor",
            "invalid": "Seleccionar la categoria de la publicacion, por favor",
        },
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        return title.lower().capitalize()

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description

    def clean_category(self):
        category = self.cleaned_data.get("category")
        if not category:
            raise ValidationError(
                "Seleccionar la categoria de la publicacion, por favor"
            )
        return category
