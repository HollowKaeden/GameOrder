from django.shortcuts import render, redirect
from utils.decorators import login_required


@login_required
def tables(request):
    if request.session.get('role') != 'admin':
        return redirect('main:index')
    template = 'admin_panel/admin.html'
    return render(request, template)
