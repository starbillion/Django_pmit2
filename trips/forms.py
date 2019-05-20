from django import forms
from django.contrib.admin import widgets
from .models import Trip

class AddTrip(forms.ModelForm):

    class Meta:
        model = Trip
        # checkin = forms.DateField(widget=AdminDateWidget())
        # checkout = forms.DateField(widget=AdminDateWidget())
        fields = '__all__'
        exclude = ['active', 'deleted_at','person','discount','savings']
        # fields = ('title', 'text',)
        
    def __init__(self, *args, **kwargs):
        super(AddTrip, self).__init__(*args, **kwargs)
        self.fields['checkin'].widget = widgets.AdminDateWidget()
        self.fields['checkout'].widget = widgets.AdminTimeWidget()
        
