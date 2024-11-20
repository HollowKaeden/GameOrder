from django.shortcuts import render
from utils.db_utils import (get_programming_languages_names,
                            get_engines_names,
                            get_genres_names)


def order(request):
    template = 'orders/order.html'

    languages = get_programming_languages_names()
    engines = get_engines_names()
    genres = get_genres_names()
    context = {
        'languages': languages,
        'engines': engines,
        'genres': genres
    }

    return render(request, template, context)


def my_orders(request):
    template = 'orders/my_orders.html'
    return render(request, template)
