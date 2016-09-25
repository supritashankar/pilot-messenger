import pusher

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.views import View

@login_required
def home(request):
    return render(request, 'chatroom/home.html',{'form': MessageForm()})


@login_required
def postmessage(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message_text = form.cleaned_data['message_text']
            channel = form.cleaned_data['channel']
            return render(request, 'chatroom/post-messages.html', {'form': MessageForm()})
    else:
        form = MessageForm()

    return render(request, 'chatroom/post-messages.html', {'form': form})
