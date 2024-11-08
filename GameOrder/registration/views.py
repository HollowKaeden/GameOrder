from django.shortcuts import render


def login(request):
    template = 'registration/login.html'
    return render(request, template)


def logout(request):
    template = 'registration/logout.html'
    return render(request, template)
