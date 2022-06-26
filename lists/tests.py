from urllib import request

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class SmokeTest(TestCase):
    def test_resolve_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        html = response.content.decode("utf8")

        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))
