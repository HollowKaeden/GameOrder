from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    template = 'registration/login.html'
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('main')
        else:
            context = {'error': 'Неверный логин или пароль'}
            return render(request, template, context)
    return render(request, template)


def logout_view(request):
    logout(request)
    return redirect('login')
