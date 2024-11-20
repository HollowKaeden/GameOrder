from django.urls import include, path

urlpatterns = [
    path('admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('registration/', include('registration.urls',
                                  namespace='registration')),
    path('', include('main.urls', namespace='main')),
]
