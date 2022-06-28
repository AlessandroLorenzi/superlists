from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        save_item(request)
        return redirect("/")

    items = Item.objects.all()
    return render(request, "lists/home.html", {"items": items})


def save_item(request):
    item = Item()
    new_item_text = request.POST.get("item_text", "")
    if new_item_text != "":
        item.text = new_item_text
        item.save()
