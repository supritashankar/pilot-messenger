from django.conf.urls import url

from views import HomeView, PostMessage

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^postmessage/$', PostMessage.as_view(), name='postmessage'),
]
