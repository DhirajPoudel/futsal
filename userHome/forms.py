from django import forms
from adminHome.models import Booking, Futsal
from django.forms.widgets import TextInput


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class TimeInput(forms.TimeInput):
    input_type = "time"


class AddBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'book_time']

    widgets = {
        'booking_date': forms.DateInput(attrs={'type': 'date'}),
        'booking_time': forms.TimeInput(attrs={'value': '2'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["booking_date"].widget = DateInput()
        self.fields["booking_time"].widget = TimeInput()

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = 'form-control'


class FutsalSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search')
    name = forms.ChoiceField(choices=[], required=False, label='Name')
    location = forms.ChoiceField(choices=[], required=False, label='Location')
    time = forms.TimeField(required=False, label='Time')
    futsal_type = forms.ChoiceField(choices=[], required=False, label='Type')
    price = forms.DecimalField(required=False, label='Price')

    def __init__(self, *args, **kwargs):
        super(FutsalSearchForm, self).__init__(*args, **kwargs)

        # Populate choices for 'name', 'location', and 'futsal_type' from the database
        all_futsals = Futsal.objects.all()

        self.fields['name'].choices = [('', '---')] + [(f['name'], f['name']) for f in all_futsals.values('name').distinct()]
        self.fields['location'].choices = [('', '---')] + [(f['location'], f['location']) for f in all_futsals.values('location').distinct()]
        self.fields['futsal_type'].choices = [('', '---')] + [(f['futsal_type'], f['futsal_type']) for f in all_futsals.values('futsal_type').distinct()]
