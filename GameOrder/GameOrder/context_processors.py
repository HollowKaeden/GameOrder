def auth_context(request):
    return {
        'is_authenticated': 'user_id' in request.session,
        'username': request.session.get('username'),
        'user_role': request.session.get('role'),
    }
