from django.views.generic import DeleteView, DetailView, ListView, TemplateView
import requests
import matplotlib.pyplot as plt
import io, base64
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import itertools
from ..forms import Req83Form
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

color_cycle= itertools.cycle(["orange","pink","blue","brown","red","grey","yellow","green"])

def generate_request(url, params={}, method = 'GET'):
    if method == 'GET':
        response = requests.get(url, params=params)
    else:
        response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()

def generate_clusters_kmeans(X, n_clusters, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0):
    X= np.array(X)
    kmeans = KMeans(n_clusters = n_clusters, init=init, max_iter = max_iter, n_init = n_init, random_state = random_state)    
    y_kmeans = kmeans.fit_predict(X)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']
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

def generate_WCSS(X, n_cluster_max = 20, n_clusters=6, init = "k-means++", max_iter = 300, n_init = 10, random_state = 0):
    X= np.array(X)
    wcss = []
    for i in range(2, n_cluster_max):
        kmeans = KMeans(n_clusters = i, init = init, max_iter = max_iter, n_init = n_init, random_state = random_state)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    
    plt.plot(range(2,20), wcss, markersize=30, lw=2)
    plt.grid(True)
    plt.title("Método del codo")
    plt.xlabel("Número de Clusters")
    plt.ylabel("WCSS(k)")
    for i, label in enumerate(wcss):
        plt.annotate(str(round(label)), (i+2, label + label/20))

    plt.scatter(range(2,20), wcss, s = 50, c = 'red', label = "Suma de la distancia cuadrada(Error)")
    plt.legend()

    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    plt.close()
    return b64


class Req83View(FormView):
    template_name = "req83.html"
    form_class = Req83Form
    success_url = reverse_lazy('base:req83')

    def form_valid(self, form, **kwargs):
        url = "http://127.0.0.1:8000/api/req83/"
        url2="https://teamjsj.herokuapp.com/api/req83/"
        context = self.get_context_data(**kwargs)
        context['form'] = form
        clusters = requests.post(url2, data={
                "n_clusters": form.cleaned_data['n_clusters'],
                "init": form.cleaned_data['init'],
                "max_iter": form.cleaned_data['max_iter'],
                "n_init": form.cleaned_data['n_init'],
                "random_state": form.cleaned_data['random_state']
            }).json()
        params = clusters['params']
        pre= pd.DataFrame(clusters['values'], columns=['Categoria', 'Cantidad', 'Cluster'])
        pre= pre.groupby(['Cluster'], as_index=False).count().drop('Categoria',axis=1)
        pre['Porcentaje']=(pre['Cantidad'] / pre['Cantidad'].sum() *100).round(2)
        if context:
            context['clusters'] = sorted(clusters['values'], key=lambda x: x[2])
            context['cantidad'] = pre.values
            context['codo'] = generate_WCSS(clusters['X'], n_cluster_max=20, **params)
            context['kmeans'] = generate_clusters_kmeans(clusters['X'], **params)
        # here you can add things like:
        
        return self.render_to_response(context)