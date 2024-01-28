from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import ProcessMessageView, SendMessageView, TaskResultViewSet

class UrlsTest(SimpleTestCase):
    def test_send_message_url_resolves(self):
        url = reverse('send_message')
        self.assertEqual(resolve(url).func.view_class, SendMessageView)

    def test_process_message_url_resolves(self):
        url = reverse('process_message')
        self.assertEqual(resolve(url).func.view_class, ProcessMessageView)

    def test_tasks_url_resolves(self):
        url = reverse('taskresult-list')  #
        self.assertEqual(resolve(url).func.cls, TaskResultViewSet)
