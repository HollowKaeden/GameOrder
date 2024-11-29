from django.urls import include, path

urlpatterns = [
    path('admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('registration/', include('registration.urls',
                                  namespace='registration')),
    path('api/', include('api.urls', namespace='api')),
    path('', include('main.urls', namespace='main')),
]
