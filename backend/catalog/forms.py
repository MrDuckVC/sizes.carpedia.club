from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import MultiWidget, MultiValueField
from django.utils.translation import gettext_lazy as _

from .models import AutoPartSizeType, Category


class RangeWidget(MultiWidget):
    """
    Widget for range field.
    It consists of two number inputs.
    """
    template_name = "catalog/widgets/range.html"

    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs=attrs),
            forms.NumberInput(attrs=attrs),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split("-")
        return [None, None]


class RangeField(MultiValueField):
    """
    Field for range.
    It consists of two integer fields.
    """
    widget = RangeWidget

    def __init__(self, **kwargs):
        min_value, max_value = kwargs.pop("min_value", None), kwargs.pop("max_value", None)
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
        )

        # Add validators to fields.
        for field in fields:
            field.validators.append(MinValueValidator(min_value))
            field.validators.append(MaxValueValidator(max_value))

        super().__init__(
            fields,
            require_all_fields=True,
            **kwargs
        )

        # To validate on the client side we need to add min and max attributes to the widget.
        for widget in self.widget.widgets:
            widget.attrs["min"] = min_value
            widget.attrs["max"] = max_value

    def compress(self, values):
        if values:
            if (values[0] is None and values[1] is not None) or (values[0] is not None and values[1] is None):
                raise ValidationError(_("Заполните оба поля или ни одного"))
            if values[0] > values[1]:
                raise ValidationError(_("Минимальное значение не может быть больше максимального"))
            if values[0] < 0 or values[1] < 0:
                raise ValidationError(_("Значения не могут быть отрицательными"))
            return f"{values[0]}-{values[1]}"
        return None


class SearchBySizesForm(forms.Form):
    """
    Search form.
    """

    def __init__(self, category: Category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        # Get any auto part from category
        for size in category.sizes.all():
            if size.type == AutoPartSizeType.INTEGER:
                self.fields[size.name] = forms.IntegerField(label=size.name, required=False, min_value=0, max_value=1024, help_text=size.description)
            elif size.type == AutoPartSizeType.RANGE:
                self.fields[size.name] = RangeField(label=size.name, required=False, min_value=0, max_value=1024, help_text=size.description)
            elif size.type == AutoPartSizeType.CHOICE:
                choices = [(choice, choice) for choice in size.data["choices"]]
                # User should be able to choose empty value:
                choices.insert(0, ("", "---------"))
                self.fields[size.name] = forms.ChoiceField(label=size.name, choices=choices, required=False, help_text=size.description)

        # set initial values from GET
        for field_name, field in self.fields.items():
            if field_name in self.data:
                field.initial = self.data[field_name]


class SearchByNumberForm(forms.Form):
    """
    Search form.
    """
    number = forms.CharField(label=_("Поиск по номеру"), required=False, max_length=50)


