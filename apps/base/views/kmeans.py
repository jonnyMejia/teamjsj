import re
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from ..forms.kmeans import KmeansForm
import requests


class KmeansView(FormView):
    template_name = "kmeans/kmeans.html"
    form_class = KmeansForm
    success_url = reverse_lazy('base:kmeans')
    extra_context = dict()
    paginate_by = 20

    def form_valid(self, form, **kwargs):

        url2 = "http://127.0.0.1:8000/kmeans/"
        url= "https://backend-teamjsj.herokuapp.com/kmeans/"         
        self.extra_context['form'] = form
        response = requests.post(url, json={
                "n_clusters": form.cleaned_data['n_clusters'],
                "init": form.cleaned_data['init'],
                "max_iter": form.cleaned_data['max_iter'],
                "n_init": form.cleaned_data['n_init'],
                "random_state": form.cleaned_data['random_state'],
                'query':form.cleaned_data['query']
            }).json()
        paginator = Paginator(response['results'], self.paginate_by)
        page_obj = paginator.get_page(1)
        self.extra_context.update(response)
        self.extra_context['page_obj'] = page_obj
  
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(KmeansView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get(self, *args, **kwargs):
        if(self.extra_context):
            paginator = Paginator(self.extra_context['results'], self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            self.extra_context['page_obj'] = page_obj
        resp = super().get(*args, **kwargs)
        return resp