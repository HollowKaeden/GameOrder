from django.shortcuts import render
from utils.db_utils import (get_programming_languages,
                            get_engines,
                            get_genres)


def order(request):
    template = 'orders/order.html'

    languages = get_programming_languages()
    engines = get_engines()
    genres = get_genres()
    context = {
        'languages': languages,
        'engines': engines,
        'genres': genres
    }

    return render(request, template, context)


def my_orders(request):
    template = 'orders/my_orders.html'
    return render(request, template)
