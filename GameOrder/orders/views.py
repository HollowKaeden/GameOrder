from django.shortcuts import render, redirect
from django.contrib import messages
from utils.decorators import login_required
from utils.db_utils import (get_programming_languages,
                            get_engines,
                            get_genres,
                            create_application)


@login_required
def order(request):
    template = 'orders/order.html'

    if request.method == 'POST':
        task = request.POST.get('task')
        language_id = request.POST.get('language')
        engine_id = request.POST.get('engine')
        genre_id = request.POST.get('genre')

        if not task or not language_id or not engine_id or not genre_id:
            messages.error(request, "Все поля должны быть заполнены.")
            return redirect('orders:order')

        user_id = request.session['user_id']
        create_application(user_id, task, language_id, engine_id, genre_id)
        return redirect('orders:my_orders')

    languages = get_programming_languages()
    engines = get_engines()
    genres = get_genres()
    context = {
        'languages': languages,
        'engines': engines,
        'genres': genres
    }

    return render(request, template, context)


@login_required
def my_orders(request):
    template = 'orders/my_orders.html'
    return render(request, template)
