from django.shortcuts import render


def tables(request):
    template = 'admin_panel/admin.html'
    return render(request, template)
