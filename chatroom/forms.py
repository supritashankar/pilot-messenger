from models import Message
from django import forms


class MessageForm(forms.ModelForm):
     class Meta:
         model = Message
         fields = ['message_text', 'post_channels', 'subscribe_channels', 'event', 'public_channel']
         widgets = {
            'message_text': forms.TextInput(attrs={'class': 'form-control'}),
            'post_channels': forms.TextInput(attrs={'class': 'form-control'}),
            'subscribe_channels': forms.HiddenInput(),
            'event': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SubscribeForm(forms.Form):
    user_input = forms.CharField(label='Channel names', max_length=100)
