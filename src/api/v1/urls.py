from django.urls import include, path

urlpatterns = [
    path('auth/', include('views.auth')),
    path('docs/', include('views.docs')),
    path('posts/', include('views.post')),
    path('users/', include('views.user')),
]
