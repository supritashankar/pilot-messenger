from django.conf.urls import url

from views import HomeView, PostMessage, UpdateMessage

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^postmessage/$', PostMessage.as_view(), name='postmessage'),
    url(r'^updatemessage/$', UpdateMessage.as_view(), name='updatemessage'),
]
