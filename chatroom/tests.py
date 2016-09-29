# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from .views import HomeView, PostMessage, UpdateMessage


class ChatroomTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staffuser = User.objects.create_user(username='supushank', email='supu@…', password='123')
        self.user = User.objects.create_superuser(username='sups', email='sups@…', password='1234')

    def test_home_view_with_anonymous_user(self):
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 302) #Returns 302 as it as redirected to login

    def test_chat_with_new_user(self):
        self.client.login(username='supushank', password='123')
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200) #Returns 200 as the person is logged in


    def test_postmessage_with_get(self):
        self.client.login(username='supushank', password='123')
        response = self.client.get('/chat/postmessage/')
        self.assertEqual(response.status_code, 405) #Returns 405 as it is not allowed in this classview

    def test_postmessage_with_post(self):
        #TODO: Stub pusher. Do not make actual calls.
        self.client.login(username='supushank', password='123')
        response = self.client.post('/chat/postmessage/',
                            {'message_text': 'hello world', 'channel_name': 'test_channel', 'event_name':'sup-hack'}, format='json')
        self.assertEqual(response.status_code, 200) #Returns 200 as it posts successfully

    def test_postmessage_with_post(self):
        #TODO: Stub pusher. Do not make actual calls.
        self.client.login(username='supushank', password='123')
        response = self.client.post('/chat/postmessage/',
                            {'message_text': 'hello world', 'channel_name': 'test_channel', 'event_name':'sup-hack'}, format='json')
        self.assertEqual(response.status_code, 200) #Returns 200 as it posts successfully
