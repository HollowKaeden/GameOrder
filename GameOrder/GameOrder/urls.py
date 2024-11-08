from django.urls import include, path

urlpatterns = [
    path('admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('order/', include('order_page.urls', namespace='order_page')),
    path('', include('registration.urls', namespace='registration'))
]
