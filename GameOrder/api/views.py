from django.http import JsonResponse
from rest_framework.decorators import api_view
from utils.db_utils import update_application, delete_application


@api_view(['PATCH'])
def api_patch_application(request, pk):
    task = request.data.get('task')
    status = request.data.get('status')
    language_id = request.data.get('language_id')
    engine_id = request.data.get('engine_id')
    genre_id = request.data.get('genre_id')

    success = update_application(
        pk, status, task, language_id, engine_id, genre_id
    )

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
