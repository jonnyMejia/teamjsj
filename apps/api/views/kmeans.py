from os import stat
from rest_framework.views import APIView
from rest_framework.response import Response
from ..controller.req83 import *
from ..serializers import KmeansSerializer
from rest_framework import status
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import itertools
import io, base64

color_cycle= itertools.cycle(["orange","pink","blue","brown","red","grey","yellow","green"])

class KmeansView(APIView):

    def get(self, request, format=None):
        
        return Response({'Algoritmo': "Kmeans"}, status=status.HTTP_200_OK)
        
    def post(self, request):

        serializer = KmeansSerializer(data=request.data)

        if serializer.is_valid():
            params = serializer.data
            dataset= pd.DataFrame(selectReq83(), columns=['Categoria', 'Titulo']).reset_index(drop=True)
            x_kmeans = dataset.apply(LabelEncoder().fit_transform).values
            x_kmeans = StandardScaler().fit_transform(x_kmeans)
            
            kmeans = KMeans(**params)   
            y_kmeans = kmeans.fit_predict(x_kmeans)
            dataset['Cluster'] = y_kmeans
            image = generate_clusters_kmeans(x_kmeans, y_kmeans, kmeans, **params)
            codo = generate_WCSS(x_kmeans, **params)
            statistics = generate_statistics(dataset)
            dataset['Numero'] = [x+1 for x in range(len(dataset))]
            
            return Response({'classifier_kmeans':params, 'results':dataset.values, 'image':image, 'codo':codo, 'statistics':statistics.values}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_statistics(dataset):
    dataset = dataset.drop(['Categoria'],axis=1)
    statistics = dataset.groupby(['Cluster'], as_index=False).count()
    statistics['Moda'] = dataset.groupby(['Cluster']).agg(lambda x:x.value_counts().index[0])
    statistics['Porcentaje']=(statistics['Titulo'] / statistics['Titulo'].sum() *100).round(2)
    statistics = statistics.sort_values('Porcentaje', ascending=False)
    statistics['Numero'] = [x+1 for x in range(len(statistics))]
    # Cluster, Count, Mode, Percentage, Numero_Id
    return statistics

def generate_clusters_kmeans(X, y_kmeans, kmeans, n_clusters, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0):
   
    for i in range(0, n_clusters):
        plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], s = 100, c = next(color_cycle), label = "Cluster " + str(i))
    plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s = 50, c = next(color_cycle), label = "Baricentros")
    
    for x, y in kmeans.cluster_centers_:
        plt.annotate(str((round(x,1), round(y,1))), (x, y))

    plt.title("Cluster de Ofertas")
    plt.xlabel("Categorias")
    plt.ylabel("Titulos de Ofertas")
    plt.legend()

    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    plt.close()
    return (b64)

def generate_WCSS(x_kmeans, n_clusters=6, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0):
    wcss = []
    for i in range(2, n_clusters*3):
        kmeans = KMeans(n_clusters = i, init = init, max_iter = max_iter, n_init = n_init, random_state = random_state)
        kmeans.fit(x_kmeans)
        wcss.append(kmeans.inertia_)
    
    plt.plot(range(2,n_clusters*3), wcss, markersize=30, lw=2)
    plt.grid(True)
    plt.title("Método del codo")
    plt.xlabel("Número de Clusters")
    plt.ylabel("WCSS(k)")
    for i, label in enumerate(wcss):
        plt.annotate(str(round(label)), (i+2, label + label/(n_clusters*3)))

    plt.scatter(range(2,n_clusters*3), wcss, s = 50, c = 'red', label = "Suma de la distancia cuadrada(Error)")
    plt.legend()

    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    plt.close()
    return b64