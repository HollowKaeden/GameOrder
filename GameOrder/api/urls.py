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
    path('user/<int:pk>/patch',
         views.api_patch_user,
         name='patch_user'),
    path('user/<int:pk>/delete',
         views.api_delete_user,
         name='delete_user'),
    path('users/',
         views.filter_users,
         name='filter_users'),
]
