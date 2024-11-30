from django.http import JsonResponse
from rest_framework.decorators import api_view
from utils.db_utils import (update_application,
                            delete_application,
                            update_user,
                            delete_user)


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


@api_view(['DELETE'])
def api_delete_application(request, pk):
    application_deleted = delete_application(pk)
    if application_deleted:
        return JsonResponse({'status': 'success', 'message': 'Задача удалена'})
    return JsonResponse({'status': 'error', 'message': 'Задача не найдена!'})


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
    application_deleted = delete_user(pk)
    if application_deleted:
        return JsonResponse({'status': 'success', 'message': 'Задача удалена'})
    return JsonResponse({'status': 'error', 'message': 'Задача не найдена!'})
