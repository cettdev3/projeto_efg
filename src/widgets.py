from email.policy import default
from django import forms
from django.utils.safestring import mark_safe
import django_tables2 as tables


class DatePickerInput(forms.DateInput):
    input_type = "date"


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime"


class DependentSelect(forms.widgets.Select):
    class Media:
        css = {}
        js = ()

    def __init__(self, attrs: None, *args, **kwargs) -> None:
        attrs = attrs or {}

        default_options = {}

        options = kwargs.get("options", {})
        default_options.update(options)
        for key, val in default.items():
            attrs["data-" + key] = val

        super().__init__(attrs)


class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return mark_safe(
            "<p><label><input %s/><span></span></label></p>" % attrs.as_html()
        )
