from django.shortcuts import render, redirect
from utils.decorators import login_required
from utils.db_utils import get_users


@login_required
def tables(request):
    if request.session.get('role') != 'admin':
        return redirect('main:index')
    template = 'admin_panel/admin.html'

    context = {'users': get_users()}

    return render(request, template, context)
