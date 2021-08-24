import re
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from requests.api import get
from ..forms.dbscan import DBScanForm
import requests

class DBScanView(FormView):
    template_name = "dbscan/dbscan.html"
    form_class = DBScanForm
    success_url = reverse_lazy('base:dbscan')
    extra_context = dict()

    def form_valid(self, form, **kwargs):
  
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(DBScanView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        return resp