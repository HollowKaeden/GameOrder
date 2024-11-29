from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('application/<int:pk>/patch',
         views.api_patch_application,
         name='patch_application'),
    path('application/<int:pk>/delete',
         views.api_delete_application,
         name='delete_application'),
]
