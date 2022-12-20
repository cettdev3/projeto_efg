from email.policy import default
from django import forms
from django.utils.safestring import mark_safe
import django_tables2 as tables

class DatePickerInput(forms.DateInput):
    input_type = 'date'

        
class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class DependentSelect(forms.widgets.Select):
    class Media:
        css = {}
        js = ()

    def __init__(self, attrs: None, *args, **kwargs) -> None:
        attrs = attrs or {}

        default_options = {}

        options = kwargs.get('options', {})
        default_options.update(options)
        for key, val in default.items():
            attrs['data-' + key] = val

        super().__init__(attrs)