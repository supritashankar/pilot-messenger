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

    def post(self, request):
        message = request.POST['message_text']
        channel = request.POST['channel_name']
        try:
            p = singleton(PusherClient)
            p.pusher_client.trigger(channel, 'my_event', {'message': message, 'user':str(request.user)})
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

class UpdateMessage(View):
    """
        Each time a message is triggered we store that in the session.
        So that even if the person refreshes the page we do not lose the previous ones.
    """
    def post(self, request):
        message = request.POST['message_text']
        user = request.POST['user']
        try:
            messages = self.request.session['messages']
            messages.append({u'message_text':message, u'user':user})
            self.request.session['messages'] = messages
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

class PusherClient(object):

    _instance = None

    def __init__(self):
        self.pusher_client = pusher.Pusher(
            app_id='252378',
            key='48eec20d8ef030076b17',
            secret='d2e330e7a270983a4430'
        )

def singleton(classname):
    """
        This function is to assure only one instance of PusherClient exists at all times.
    """
    if not classname._instance:
        classname._instance = classname()
    return classname._instance
