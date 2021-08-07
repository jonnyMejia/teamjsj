from django.urls import path, include

urlpatterns = [
    path('kmeans/', include('apps.api.urls.kmeans')),
]
