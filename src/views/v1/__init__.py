from django.urls import include, path

urlpatterns = [
    path('auth/', include('views.v1.auth')),
    path('docs/', include('views.v1.docs')),
    path('posts/', include('views.v1.post')),
    path('users/', include('views.v1.user')),
]
