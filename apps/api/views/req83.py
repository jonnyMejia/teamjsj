from rest_framework.views import APIView
from rest_framework.response import Response
from ..controller.req83 import *
from rest_framework import status
from ..serializers import Req83Serializer
import pandas as pd
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

class Req83ListView(APIView):

    def get(self, request, format=None):
        serializer = Req83Serializer(data=request.data)

        if serializer.is_valid():
            dataset= pd.DataFrame(selectReq83(), columns=['Categoria', 'Titulo']).reset_index(drop=True)
            X = dataset.apply(LabelEncoder().fit_transform).values
            data = serializer.data
        
            sc_x = StandardScaler()
            # Se establece una transformacion
            X = sc_x.fit_transform(X)

            kmeans = KMeans(**data)    
            y_kmeans = kmeans.fit_predict(X)
            
            dataset['Cluster'] = y_kmeans
            return Response({'values':dataset.values, 'X':X, 'params':data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        serializer = Req83Serializer(data=request.data)

        if serializer.is_valid():
            dataset= pd.DataFrame(selectReq83(), columns=['Categoria', 'Titulo']).reset_index(drop=True)
            X = dataset.apply(LabelEncoder().fit_transform).values
            data = serializer.data
        
            sc_x = StandardScaler()
            # Se establece una transformacion
            X = sc_x.fit_transform(X)

            kmeans = KMeans(**data)    
            y_kmeans = kmeans.fit_predict(X)
            
            dataset['Cluster'] = y_kmeans
            return Response({'values':dataset.values, 'X':X, 'params':data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

