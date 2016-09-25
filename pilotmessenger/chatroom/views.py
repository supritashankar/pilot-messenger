import pusher

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views import View

class HomeView(TemplateView):
    template_name = "chatroom/home.html"
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context


class PostMessage(View):
    def get(self, request):
        return render(request, 'chatroom/post-messages.html', {'form': MessageForm()})

    def post(self, request):
        message = request.POST['message_text']
        channel = request.POST['channel_name']
        pusher_client = pusher.Pusher(
            app_id='251400',
            key='a4cc9d7318ae0879ac0b',
            secret='6dd89d34ce25d9ee23f4',
            ssl=True
        )
        pusher_client.trigger(channel, 'my_event', {'message': message})
        return render(request, 'chatroom/post-messages.html', {'form': MessageForm()})
