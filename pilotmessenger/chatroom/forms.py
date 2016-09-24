from models import Message
from django.forms import ModelForm


class MessageForm(ModelForm):
     class Meta:
         model = Message
         fields = ['message_text', 'channel', 'public_channel']
