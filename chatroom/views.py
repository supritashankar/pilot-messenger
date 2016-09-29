import pusher
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from forms import MessageForm, SubscribeForm
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
            messages = []

        try:
            channels = self.request.session['channels']
        except:
            channels = ['test-channel']


        self.request.session['messages'] = messages
        self.request.session['channels'] = channels

        ## Send the form and initial messages in the context ##
        context['messages'] = self.request.session['messages']
        context['form'] = MessageForm(initial={'subscribe_channels': channels})
        return context


class PostMessage(View):

    def post(self, request):
        message = request.POST['message_text']
        channel = request.POST['channel_name'].split(',')
        event = request.POST['event_name']
        try:
            p = singleton(PusherClient)
            p.pusher_client.trigger(channel, event,
                    {'message': message, 'user':str(request.user), 'channel':','.join(channel)})
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

class UpdateMessage(View):
    """
        Each time a message is triggered we store that in the session.
        So that even if the person refreshes the page we do not lose the previous ones.
    """
    def post(self, request):
        message = request.POST.get('message_text', 'Error!')
        user = request.POST.get('user', 'no user')
        channel = request.POST.get('channel', 'no channel')
        try:
            messages = self.request.session['messages']
            messages.append({u'message_text':message, u'user':user, u'channel':channel})
            self.request.session['messages'] = messages
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

class PusherAuth(View):
    """ Auth view to subscribe to private channels within Pusher
    """
    def post(self, request):
        auth = pusher.authenticate(
            channel=request.form['channel_name'],
            socket_id=request.form['socket_id']
        )
        return json.dumps(auth)

class Subscribe(View):
    """
        A subscribe view which lets the user decide which channels he wants
        to subscribe to.
    """

    def get(self, request):
        context = {'form': SubscribeForm()}
        return render(request, 'chatroom/subscribe.html', context)

    def post(self, request):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            channels = form.cleaned_data['user_input']
            self.request.session['channels'] = channels
            return redirect('index')
        return render(request, 'chatroom/subscribe.html', {'form':SubscribeForm()})


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
    """
        This function is to assure only one instance of PusherClient exists at all times.
    """
    if not classname._instance:
        classname._instance = classname()
    return classname._instance
