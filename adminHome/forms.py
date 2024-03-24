from django import forms
from .models import Futsal
from django.forms.widgets import TextInput

class TimeInput(forms.TimeInput):
    input_type = "time"

class AddFutsalForm(forms.ModelForm):
    class Meta:
        model = Futsal
        fields = ['name', 'images', 'futsal_type', 'location', 'price', 'open_time', 'close_time', 'contact_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["open_time"].widget = TimeInput()
        self.fields["close_time"].widget = TimeInput()

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
