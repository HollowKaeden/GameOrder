from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('users/<int:pk>/patch',
         views.api_patch_user,
         name='patch_user'),
    path('users/<int:pk>/delete',
         views.api_delete_user,
         name='delete_user'),
    path('users/',
         views.filter_users,
         name='filter_users'),
    path('users/add',
         views.add_user,
         name='add_user'),
    path('contacts/<int:pk>/patch',
         views.api_patch_contact,
         name='patch_contact'),
    path('contacts/<int:pk>/delete',
         views.api_delete_contact,
         name='delete_contact'),
    path('contacts/',
         views.filter_contacts,
         name='filter_contacts'),
    path('application/<int:pk>/patch',
         views.api_patch_application,
         name='patch_application'),
    path('application/<int:pk>/delete',
         views.api_delete_application,
         name='delete_application'),
]
