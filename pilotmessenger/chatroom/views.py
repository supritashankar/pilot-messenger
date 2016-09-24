import pusher

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        # pusher_client = pusher.Pusher(
        #   app_id='251400',
        #   key='a4cc9d7318ae0879ac0b',
        #   secret='6dd89d34ce25d9ee23f4',
        #   ssl=True
        # )

        if form.is_valid():
            print form.cleaned_data['message_text']
            return HttpResponseRedirect('/thanks/')
    else:
        form = MessageForm()

    return render(request, 'chatroom/index.html', {'form': form})
