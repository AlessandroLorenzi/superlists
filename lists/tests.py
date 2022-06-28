from urllib import request

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page


class SmokeTest(TestCase):
    def test_resolve_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        html = response.content.decode("utf8")

        self.assertIn('<html lang="en">', html)
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>\n"))

    def test_use_case_get(self):
        self.client.get("/")
        self.assertTemplateUsed("lists/home.html")

    def test_can_save_a_post_request(self):
        self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_dont_save_empty_items(self):
        self.client.post("/", data={"item_text": ""})
        self.assertEqual(Item.objects.count(), 0)

    def test_redirect_after_save_item(self):
        response = self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_displays_all_list_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/")

        self.assertIn("itemey 1", response.content.decode())
        self.assertIn("itemey 2", response.content.decode())


class ItemModelTest(TestCase):
    def test_save_and_retrieve_item(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second list item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "The first (ever) list item")
        self.assertEqual(saved_items[1].text, "The second list item")
