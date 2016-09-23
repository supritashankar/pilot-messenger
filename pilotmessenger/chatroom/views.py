from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('chatroom/index.html')
    context = {
        'latest_message': True,
    }
    return HttpResponse(template.render(context, request))
