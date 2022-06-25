from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class SmokeTest(TestCase):
    def test_resolve_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

