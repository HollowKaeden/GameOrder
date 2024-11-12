from django.urls import include, path

urlpatterns = [
    path('admin/', include('admin_panel.urls', namespace='admin_panel')),
    path('order/', include('order_page.urls', namespace='order_page')),
    path('registration/', include('registration.urls',
                                  namespace='registration')),
    path('', include('main.urls', namespace='main')),
]
