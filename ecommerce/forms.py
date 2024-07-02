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
    point_cost = forms.IntegerField(
        label="Coste de puntos",
        error_messages={
            "required": "Ingresar el costo de puntos, por favor",
        },
    )
    stock = forms.IntegerField(
        label="Stock",
        error_messages={
            "required": "Ingresar el sotck, por favor"
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
    
    def clean_point_cost(self):
        point_cost = self.cleaned_data.get("point_cost")
        if(point_cost <= 0):
            raise ValidationError(
                "El coste de puntos ingresado es inválido. Debe ser positivo.")   
        return point_cost
    
    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if(stock <= 0):
            raise ValidationError(
                "El stock ingresado es inválido. Debe ser positivo.")            
        return stock
    
class edit_Form(forms.Form):
    title = forms.CharField(label="Titulo", required=False)
    description = forms.CharField(label="Descripcion", required=False)
    category = forms.ModelChoiceField(label="Categoria", required=False, queryset=ProductCategory.objects.all())
    point_cost = forms.IntegerField(label="Coste de puntos", required=False)
    stock = forms.IntegerField(label="Stock", required=False)
    image = forms.ImageField(label="Image", required=False)

    def clean_title(self):
        new_title = self.cleaned_data.get('title')
        if not new_title:
            return new_title
        if len(new_title) <= 0:
            raise ValidationError("Ingrese un titulo.")
        if len(new_title) > 20:
            raise ValidationError("El titulo debe ser menor a 20 caracteres")
        return new_title

    def clean_description(self):
        new_description = self.cleaned_data.get('description')
        if not new_description:
            return new_description
        if len(new_description) <= 0:
            raise ValidationError("Ingrese una descripcion.")
        if len(new_description) > 300:
            raise ValidationError("La descripcción debe ser menor a 300 caracteres")
        return new_description


    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category
    
    def clean_point_cost(self):
        new_point_cost = self.cleaned_data.get('point_cost')
        if new_point_cost is None:
            return new_point_cost
        if new_point_cost <= 0:
            raise ValidationError("Ingrese un coste de puntos positivo.")
        return new_point_cost
    
    def clean_stock(self):
        new_stock = self.cleaned_data.get('stock')
        if new_stock is None:
            return new_stock
        if new_stock <= 0:
            raise ValidationError("Ingrese un stock positivo.")
        return new_stock
    
    def clean_image(self):
        new_image = self.cleaned_data.get('image')
        if not new_image:
            return new_image
        return new_image