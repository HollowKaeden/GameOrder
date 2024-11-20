from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from utils.db_utils import create_user, get_user_by_username


def register_view(request):
    template = 'registration/registration.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        role = 'user'

        create_user(username, password, full_name, role)

        return redirect('registration:login')

    return render(request, template)


def login_view(request):
    template = 'registration/login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = get_user_by_username(username)
        if user and check_password(password, user[2]):
            request.session['user_id'] = user[0]
            request.session['username'] = user[1]
            request.session['role'] = user[4]
            return redirect('main:index')
        else:
            context = {'error': 'Неверный логин или пароль'}
            return render(request, template, context)
    return render(request, template)


def logout_view(request):
    request.session.flush()
    return redirect('registration:login')
