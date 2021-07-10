from django.urls import path
from apps.base.views import Home, Req83View
# from apps.kmeans.views import UserListApiView, UserDetailApiView 

app_name = 'base'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('req83/', Req83View.as_view(), name='req83'),
]
