from .models import Message
from django import forms
from crispy_forms.helper import FormHelper

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'message',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
