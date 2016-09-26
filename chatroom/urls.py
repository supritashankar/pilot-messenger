from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from views import HomeView, PostMessage, UpdateMessage

urlpatterns = [
    url(r'^$', login_required(HomeView.as_view()), name='index'),
    url(r'^postmessage/$', login_required(PostMessage.as_view()), name='postmessage'),
    url(r'^updatemessage/$', login_required(UpdateMessage.as_view()), name='updatemessage'),
]
