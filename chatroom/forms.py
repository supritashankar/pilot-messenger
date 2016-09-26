from models import Message
from django import forms


class MessageForm(forms.ModelForm):
     class Meta:
         model = Message
         fields = ['message_text', 'channel', 'public_channel']
         widgets = {
            'message_text': forms.TextInput(attrs={'class': 'form-control'}),
            'channel': forms.TextInput(attrs={'class': 'form-control'}),
        }
