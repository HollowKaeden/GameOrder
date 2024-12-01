from django.shortcuts import render, redirect
from utils.decorators import login_required
from utils.db_utils import (get_users,
                            get_contacts,
                            get_user_application_connects)


@login_required
def tables(request):
    if request.session.get('role') != 'admin':
        return redirect('main:index')
    template = 'admin_panel/admin.html'

    context = {
        'users': get_users(),
        'contacts': get_contacts(),
        'connections': get_user_application_connects(),
    }

    return render(request, template, context)
