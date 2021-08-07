from django.urls import path
from apps.api.views.kmeans import KmeansView
# from apps.kmeans.views import UserListApiView, UserDetailApiView 

app_name = 'kmeans'

urlpatterns = [
    path('', KmeansView.as_view(), name='list'),
]
