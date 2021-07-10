from django.urls import path
from apps.api.views.req83 import Req83ListView
# from apps.kmeans.views import UserListApiView, UserDetailApiView 

app_name = 'req83'

urlpatterns = [
    path('', Req83ListView.as_view(), name='list'),
]
