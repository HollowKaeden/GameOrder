from django.http import JsonResponse
from rest_framework.decorators import api_view
from utils.db_utils import (get_users,
                            create_user,
                            update_user,
                            delete_user,
                            get_contacts,
                            update_contact,
                            delete_contact,
                            get_user_application_connects,
                            create_connection,
                            delete_connection,
                            get_applications,
                            update_application,
                            create_application_only,
                            delete_application,
                            )


@api_view(['POST'])
def filter_users(request):
    filters = {
        'userid': request.data.get('id'),
        'username': request.data.get('username'),
        'fullname': request.data.get('fullname'),
        'role': request.data.get('role')
    }

    users = get_users(filters)
    return JsonResponse({'users': users})


@api_view(['POST'])
def add_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    full_name = request.data.get('fullname')
    role = 'user'
    phone_number = request.data.get('phone_number')
    email = request.data.get('email')

    create_user(username, password, full_name, role, phone_number, email)

    return JsonResponse({'status': 'success'})


@api_view(['PATCH'])
def api_patch_user(request, pk):
    parameters = {
        'username': request.data.get('username'),
        'password': request.data.get('password'),
        'fullname': request.data.get('fullname'),
        'role': request.data.get('role')
    }

    success = update_user(pk, parameters)

    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Пользователь не найден!'}, status=404)
    return JsonResponse({'status': 'success',
                         'message': 'Пользователь обновлен!'})


@api_view(['DELETE'])
def api_delete_user(request, pk):
    user_deleted = delete_user(pk)
    if user_deleted:
        return JsonResponse({'status': 'success', 'message': 'Задача удалена'})
    return JsonResponse({'status': 'error', 'message': 'Задача не найдена!'})


@api_view(['POST'])
def filter_contacts(request):
    filters = {
        'userid': request.data.get('id'),
        'phonenumber': request.data.get('phonenumber'),
        'email': request.data.get('email')
    }

    contacts = get_contacts(filters)
    return JsonResponse({'contacts': contacts})


@api_view(['PATCH'])
def api_patch_contact(request, pk):
    parameters = {
        'phone_number': request.data.get('PhoneNumber'),
        'email': request.data.get('Email')
    }

    success = update_contact(pk, parameters)

    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Контакт не найден!'}, status=404)
    return JsonResponse({'status': 'success',
                         'message': 'Контакт обновлен!'})


@api_view(['DELETE'])
def api_delete_contact(request, pk):
    contact_deleted = delete_contact(pk)
    if contact_deleted:
        return JsonResponse({'status': 'success', 'message': 'Задача удалена'})
    return JsonResponse({'status': 'error', 'message': 'Задача не найдена!'})


@api_view(['POST'])
def filter_connections(request):
    filters = {
        'userid': request.data.get('userid'),
        'applicationid': request.data.get('applicationid')
    }

    connections = get_user_application_connects(filters)
    return JsonResponse({'connections': connections})


@api_view(['POST'])
def add_connection(request):
    userid = request.data.get('userid')
    applicationid = request.data.get('applicationid')

    create_connection(userid, applicationid)

    return JsonResponse({'status': 'success'})


@api_view(['DELETE'])
def api_delete_connection(request):
    userid = request.data.get('userid')
    applicationid = request.data.get('applicationid')

    connection_deleted = delete_connection(userid, applicationid)
    if connection_deleted:
        return JsonResponse({'status': 'success',
                             'message': 'Соединение удалено'})
    return JsonResponse({'status': 'error',
                         'message': 'Соединение не найдено!'})


@api_view(['GET'])
def api_get_applications(request):
    applications = get_applications()
    return JsonResponse({'applications': applications})


@api_view(['POST'])
def api_filter_applications(request):
    filters = {
        'applicationid': request.data.get('applicationid'),
        'task': request.data.get('task'),
        'status': request.data.get('status'),
        'languageid': request.data.get('languageid'),
        'engineid': request.data.get('engineid'),
        'genreid': request.data.get('genreid')
    }

    applications = get_applications(filters)

    return JsonResponse({'applications': applications})


@api_view(['PATCH'])
def api_patch_application(request, pk):
    parameters = {
        'task': request.data.get('task'),
        'status': request.data.get('status'),
        'languageid': request.data.get('language_id'),
        'engineid': request.data.get('engine_id'),
        'genreid': request.data.get('genre_id')
    }

    success = update_application(pk, parameters)

    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Заявка не найдена!'}, status=404)
    return JsonResponse({'status': 'success', 'message': 'Заявка обновлена!'})


@api_view(['POST'])
def add_application(request):
    status = request.data.get('status')
    task = request.data.get('task')
    languageid = request.data.get('languageid')
    engineid = request.data.get('engineid')
    genreid = request.data.get('genreid')

    create_application_only(status, task, languageid, engineid, genreid)

    return JsonResponse({'status': 'success'})


@api_view(['DELETE'])
def api_delete_application(request, pk):
    application_deleted = delete_application(pk)
    if application_deleted:
        return JsonResponse({'status': 'success', 'message': 'Задача удалена'})
    return JsonResponse({'status': 'error', 'message': 'Задача не найдена!'})
