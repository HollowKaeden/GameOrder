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
                            get_genres,
                            update_genre,
                            create_genre,
                            delete_genre,
                            get_engines,
                            update_engine,
                            create_engine,
                            delete_engine,
                            get_programming_languages,
                            update_language,
                            create_language,
                            delete_language
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


@api_view(['GET'])
def api_get_genres(request):
    genres = get_genres()
    return JsonResponse({'genres': genres})


@api_view(['POST'])
def api_filter_genres(request):
    filters = {
        'genreid': request.data.get('genreid'),
        'name': request.data.get('name'),
        'description': request.data.get('description')
    }
    print(filters)

    genres = get_genres(filters)

    return JsonResponse({'genres': genres})


@api_view(['PATCH'])
def api_patch_genres(request, pk):
    parameters = {
        'name': request.data.get('name'),
        'description': request.data.get('description')
    }

    success = update_genre(pk, parameters)

    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Жанр не найден!'}, status=404)
    return JsonResponse({'status': 'success', 'message': 'Жанр обновлен!'})


@api_view(['POST'])
def add_genre(request):
    name = request.data.get('name')
    description = request.data.get('description')

    create_genre(name, description)

    return JsonResponse({'status': 'success'})


@api_view(['DELETE'])
def api_delete_genre(request, pk):
    genre_deleted = delete_genre(pk)
    if genre_deleted:
        return JsonResponse({'status': 'success', 'message': 'Жанр удален'})
    return JsonResponse({'status': 'error', 'message': 'Жанр не найден!'})


@api_view(['GET'])
def api_get_engines(request):
    engines = get_engines()
    return JsonResponse({'engines': engines})


@api_view(['POST'])
def api_filter_engines(request):
    filters = {
        'engineid': request.data.get('engineid'),
        'name': request.data.get('name'),
        'techfeatures': request.data.get('description')
    }

    engines = get_engines(filters)

    return JsonResponse({'engines': engines})


@api_view(['PATCH'])
def api_patch_engines(request, pk):
    parameters = {
        'name': request.data.get('name'),
        'techfeatures': request.data.get('description')
    }

    success = update_engine(pk, parameters)

    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Движок не найден!'}, status=404)
    return JsonResponse({'status': 'success', 'message': 'Движок обновлен!'})


@api_view(['POST'])
def add_engine(request):
    name = request.data.get('name')
    description = request.data.get('description')

    create_engine(name, description)

    return JsonResponse({'status': 'success'})


@api_view(['DELETE'])
def api_delete_engine(request, pk):
    engine_deleted = delete_engine(pk)
    if engine_deleted:
        return JsonResponse({'status': 'success', 'message': 'Движок удален'})
    return JsonResponse({'status': 'error', 'message': 'Движок не найден!'})


@api_view(['GET'])
def api_get_languages(request):
    languages = get_programming_languages()
    return JsonResponse({'languages': languages})


@api_view(['POST'])
def api_filter_languages(request):
    filters = {
        'languageid': request.data.get('languageid'),
        'name': request.data.get('name'),
        'description': request.data.get('description')
    }

    languages = get_programming_languages(filters)

    return JsonResponse({'languages': languages})


@api_view(['PATCH'])
def api_patch_languages(request, pk):
    parameters = {
        'name': request.data.get('name'),
        'description': request.data.get('description')
    }

    success = update_language(pk, parameters)

    if not success:
        return JsonResponse({'status': 'error',
                             'message': 'Язык не найден!'}, status=404)
    return JsonResponse({'status': 'success', 'message': 'Язык обновлен!'})


@api_view(['POST'])
def add_language(request):
    name = request.data.get('name')
    description = request.data.get('description')

    create_language(name, description)

    return JsonResponse({'status': 'success'})


@api_view(['DELETE'])
def api_delete_language(request, pk):
    language_deleted = delete_language(pk)
    if language_deleted:
        return JsonResponse({'status': 'success', 'message': 'Язык удален'})
    return JsonResponse({'status': 'error', 'message': 'Язык не найден!'})
