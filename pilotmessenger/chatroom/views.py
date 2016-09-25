import pusher

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from forms import MessageForm
from django.views.generic.base import TemplateView
from django.views import View

class HomeView(TemplateView):
    template_name = "chatroom/home.html"
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        ## Update the intial view with the previous messages ##
        try:
            messages = self.request.session['messages']
        except:
            self.request.session['messages'] = []
            messages = []
        self.request.session['messages'] = messages

        ## Send the form and initial messages in the context ##
        context['messages'] = self.request.session['messages']
        context['form'] = MessageForm()
        return context


class PostMessage(View):
    def get(self, request):
        return render(request, 'chatroom/post-messages.html', {'form': MessageForm()})

    def post(self, request):
        message = request.POST['message_text']
        channel = request.POST['channel_name']
        try:
            p = singleton(PusherClient)
            p.pusher_client.trigger(channel, 'my_event', {'message': message})
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

class UpdateMessage(View):
    def post(self, request):
        message = request.POST['message_text']
        messages = self.request.session['messages']
        messages.append({u'message_text':message})
        self.request.session['messages'] = messages
        return HttpResponse(status=200)

class PusherClient(object):
    _instance = None
    def __init__(self):
        self.pusher_client = pusher.Pusher(
            app_id='251400',
            key='a4cc9d7318ae0879ac0b',
            secret='6dd89d34ce25d9ee23f4',
            ssl=True
        )

def singleton(classname):

    if not classname._instance:
        classname._instance = classname()
    return classname._instance
